# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from kafka import KafkaProducer   #引入包，如果你在自己的电脑上跑，得先安装kafka
import time
import json

class BaiduspiderPipeline(object):
    maxCount = 50
    counter = 0
    urlList = []
    deltaList=[]
    def process_item(self, item, spider):

        if(self.counter<self.maxCount):#记录前maxCountUrl
            self.counter = self.counter + 1
            id = item['UrlId'].split('/')[4]
            self.urlList.append(id)
        return item
    def close_spider(self,spider):
        #以下实现增量爬取
        #1.得到两次数据的差集
        self.f = open("UrlList.json", "r", encoding='UTF-8')#读取josn中的上次前50个链接
        load = json.load(self.f)
        self.deltaList = list(set(load) ^ set(self.urlList))#取差集
        self.f.close()
        #2.将此次数据存入json
        self.f = open("UrlList.json", "w", encoding='UTF-8')
        content = json.dumps(self.urlList, ensure_ascii=False)
        self.f.write(content)
        self.f.close()
        #3.将差值列表存入josn
        # self.f = open("DeltaList.json", "w", encoding='UTF-8')
        # content = json.dumps(self.deltaList, ensure_ascii=False)
        # self.f.write(content)
        # self.f.close()




    def Kafka_fun(self):
        # 创建一个生产者，连接到指定的消息队列上
        producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])

        # 数据类型，假设这个为单条数据
        dict1 = list(self.deltaList)
        while True:
            msg = str(dict1)  # 将数据转成字符串
            print(msg)
            # 发送topic为information的数据（information相当于表名，每条数据记录相当于表中的一行）
            producer.send('information', msg.encode('utf-8'))
            time.sleep(1)
        # 停止生产数据
        producer.close()
