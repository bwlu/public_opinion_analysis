# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json

class BaiduspiderPipeline(object):
    maxCount = 1000 #可根据具体情况，调整存入json的id条数
    counter = 0
    urlList = []
    deltaList=[]
    templist = []
    def __init__(self):

        self.f = open("UrlList.json", "r", encoding='UTF-8')  # 读取josn中的上次的链接
        self.urlList = json.load(self.f)#将数据存入列表

    def process_item(self, item, spider):

        #记录id并存在urlList
        if(item["IsLimitedTime"]=="y"):
            if(self.counter<self.maxCount):#记录前maxCountUrl
                self.counter = self.counter + 1
                id = item['UrlId'].split('/')[4]#得到urlid
                self.templist.append(id)
            #比对id找到增量，并存入Kafka
            id = item['UrlId'].split('/')[4]
            if id not in self.urlList:
                self.deltaList.append(id)
                self.Kafka_fun(item)
        return item
    def close_spider(self,spider):
        self.urlList = self.templist
        #将数据写入文件
        self.f = open("UrlList.json", "w", encoding='UTF-8')
        content = json.dumps(self.urlList, ensure_ascii=False)
        self.f.write(content)
        self.f.close()
        #将差值列表存入josn
        self.f = open("DeltaList.json", "w", encoding='UTF-8')
        content = json.dumps(self.deltaList, ensure_ascii=False)
        self.f.write(content)
        self.f.close()

from kafka import KafkaProducer   #引入包，如果你在自己的电脑上跑，得先安装kafka
    def Kafka_fun(self,item):
        # 创建一个生产者，连接到指定的消息队列上
        producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])

        # 数据类型，假设这个为单条数据
        dict1 = list(item)
        while True:
            msg = str(dict1)  # 将数据转成字符串
            print(msg)
            # 发送topic为information的数据（information相当于表名，每条数据记录相当于表中的一行）
            producer.send('information', msg.encode('utf-8'))
            time.sleep(1)
        # 停止生产数据
        producer.close()
