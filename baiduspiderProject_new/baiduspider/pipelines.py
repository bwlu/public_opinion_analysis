# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json
from kafka import KafkaProducer   #引入包，如果你在自己的电脑上跑，得先安装kafka
global producer
class BaiduspiderPipeline(object):
    maxCount = 1000 #可根据具体情况，调整存入json的id条数
    counter = 0
#百度列表
    urlList_baidu = []
    deltaList_baidu=[]
    templist_baidu = []
#家电维修供求部分列表
    urlList_jdwxgq = []
    deltaList_jdwxgq = []
    templist_jdwxgq = []
#家电维修表彰部分列表
    urlList_jdwxbz = []
    deltaList_jdwxbz = []
    templist_jdwxbz = []
#家电维修投诉部分列表
    urlList_jdwxts = []
    deltaList_jdwxts = []
    templist_jdwxts = []
# 家电维修公告部分列表
    urlList_jdwxgg = []
    deltaList_jdwxgg = []
    templist_jdwxgg = []
# 卫视中国家电列表
    urlList_wszgjd = []
    deltaList_wszgjd = []
    templist_wszgjd = []
# 卫视中国电视列表
    urlList_wszgds = []
    deltaList_wszgds = []
    templist_wszgds = []
# 卫视中国参数直通车列表
    urlList_wszgcs = []
    deltaList_wszgcs = []
    templist_wszgcs = []
# 卫视中国综合列表
    urlList_wszgzh = []
    deltaList_wszgzh = []
    templist_wszgzh = []
# 户户通交流列表
    urlList_hhtjl = []
    deltaList_hhtjl = []
    templist_hhtjl = []
# 户户通测试列表
    urlList_hhtcs = []
    deltaList_hhtcs = []
    templist_hhtcs = []
# 户户通需求列表
    urlList_hhtxq = []
    deltaList_hhtxq = []
    templist_hhtxq = []
# 户户通故障列表
    urlList_hhtgz = []
    deltaList_hhtgz = []
    templist_hhtgz = []
    def __init__(self):
        global producer
        producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])
  
        self.urlList_baidu = self.read_file("./jsonfile/baidu_UrlList.json")
        #家电维修
        self.urlList_jdwxgq = self.read_file("./jsonfile/jdwxgq_UrlList.json")
        self.urlList_jdwxbz = self.read_file("./jsonfile/jdwxbz_UrlList.json")
        self.urlList_jdwxts = self.read_file("./jsonfile/jdwxts_UrlList.json")
        self.urlList_jdwxgg = self.read_file("./jsonfile/jdwxgg_UrlList.json")
        #卫视中国
        self.urlList_wszgjd = self.read_file("./jsonfile/wszgjd_UrlList.json")
        self.urlList_wszgds = self.read_file("./jsonfile/wszgds_UrlList.json")
        self.urlList_wszgcs = self.read_file("./jsonfile/wszgcs_UrlList.json")
        self.urlList_wszgzh = self.read_file("./jsonfile/wszgzh_UrlList.json")
        #户户通
        self.urlList_hhtjl = self.read_file("./jsonfile/hhtjl_UrlList.json")
        self.urlList_hhtcs = self.read_file("./jsonfile/hhtcs_UrlList.json")
        self.urlList_hhtxq = self.read_file("./jsonfile/hhtxq_UrlList.json")
        self.urlList_hhtgz = self.read_file("./jsonfile/hhtgz_UrlList.json")

    def process_item(self, item, spider):

        if(spider.name == 'sbaidu'):
            #记录id并存在urlList
            if(item["IsLimitedTime"]=="y"):
                if(self.counter<self.maxCount):#记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[4]#得到urlid
                    self.templist_baidu.append(id)
                #比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[4]
                try:
                    if id not in self.urlList_baidu:
                        print("111111111111111111111111111111111111111111111111")
                        self.deltaList_baidu.append(id)
                        self.Kafka_fun(item,spider.name)
                except:
                    print(22222222222222222222222222222222)
                    self.deltaList_baidu.append(id)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'jdwxgq'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_jdwxgq.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:#首次添加的异常处理
                    if num not in self.urlList_jdwxgq:
                        print("111111111111111111111111111111111111111111111111")
                        self.deltaList_jdwxgq.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    print(22222222222222222222222222222222)
                    self.deltaList_jdwxgq.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'jdwxbz'):
            if (item["IsLimitedTime"] == "y" and item['UrlId'] != None):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_jdwxbz.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:#首次添加的异常处理
                    if num not in self.urlList_jdwxbz:
                        self.deltaList_jdwxbz.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_jdwxbz.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'jdwxts'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_jdwxts.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:#首次添加的异常处理
                    if num not in self.urlList_jdwxts:
                        self.deltaList_jdwxts.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_jdwxts.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'jdwxgg'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_jdwxgg.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_jdwxgg:
                        print("1111111111111111111111111111111")
                        self.deltaList_jdwxgg.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    print("22222222222222222222222")
                    self.deltaList_jdwxgg.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'wszgjd'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_wszgjd.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgjd:
                        self.deltaList_wszgjd.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_wszgjd.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'wszgds'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_wszgds.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgds:
                        self.deltaList_wszgds.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_wszgds.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'wszgcs'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_wszgcs.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgcs:
                        self.deltaList_wszgcs.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_wszgcs.append(num)
                    self.Kafka_fun(item,spider.name)
        if(spider.name == 'wszgzh'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_wszgzh.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgzh:
                        self.deltaList_wszgzh.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_wszgzh.append(num)
                    self.Kafka_fun(item,spider.name)
        if (spider.name == 'hhtjl'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_hhtjl.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtjl:
                        self.deltaList_hhtjl.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_hhtjl.append(num)
                    self.Kafka_fun(item,spider.name)
        if (spider.name == 'hhtcs'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_hhtcs.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtcs:
                        self.deltaList_hhtcs.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_hhtcs.append(num)
                    self.Kafka_fun(item,spider.name)
        if (spider.name == 'hhtxq'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_hhtxq.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtxq:
                        self.deltaList_hhtxq.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_hhtxq.append(num)
                    self.Kafka_fun(item,spider.name)
        if (spider.name == 'hhtgz'):
            if (item["IsLimitedTime"] == "y"):
                if (self.counter < self.maxCount):  # 记录前maxCountUrl
                    self.counter = self.counter + 1
                    id = item['UrlId'].split('/')[3]  # 得到urlid
                    num = id.split('-')[1]
                    self.templist_hhtgz.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtgz:
                        self.deltaList_hhtgz.append(num)
                        self.Kafka_fun(item,spider.name)
                except:
                    self.deltaList_hhtgz.append(num)
                    self.Kafka_fun(item,spider.name)
        return item
    def close_spider(self,spider):
        if(spider.name =='sbaidu'):
            self.urlList_baidu = self.templist_baidu
            #将数据写入文件
            self.write_file("./jsonfile/baidu_UrlList.json",self.urlList_baidu)
            #将差值列表存入josn
            self.write_file("./jsonfile/baidu_DeltaList.json",self.deltaList_baidu)
        if(spider.name == 'jdwxgq'):
            self.urlList_jdwxgq = self.templist_jdwxgq
            # 将数据写入文件
            self.write_file("./jsonfile/jdwxgq_UrlList.json", self.urlList_jdwxgq)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxgq_DeltaList.json", self.deltaList_jdwxgq)
        if(spider.name == 'jdwxbz'):
            self.urlList_jdwxbz = self.templist_jdwxbz
            # 将数据写入文件
            self.write_file("./jsonfile/jdwxbz_UrlList.json", self.urlList_jdwxbz)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxbz_DeltaList.json", self.deltaList_jdwxbz)
        if(spider.name == 'jdwxts'):
            self.urlList_jdwxts = self.templist_jdwxts
            # 将数据写入文件
            self.write_file("./jsonfile/jdwxts_UrlList.json", self.urlList_jdwxts)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxts_DeltaList.json", self.deltaList_jdwxts)
        if(spider.name == 'jdwxgg'):
            self.urlList_jdwxgg = self.templist_jdwxgg
            # 将数据写入文件
            self.write_file("./jsonfile/jdwxgg_UrlList.json", self.urlList_jdwxgg)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxgg_DeltaList.json", self.deltaList_jdwxgg)
        if(spider.name == 'wszgjd'):
            self.urlList_wszgjd = self.templist_wszgjd
            # 将数据写入文件
            self.write_file("./jsonfile/wszgjd_UrlList.json", self.urlList_wszgjd)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgjd_DeltaList.json", self.deltaList_wszgjd)
        if(spider.name == 'wszgds'):
            self.urlList_wszgds = self.templist_wszgds
            # 将数据写入文件
            self.write_file("./jsonfile/wszgds_UrlList.json", self.urlList_wszgds)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgds_DeltaList.json", self.deltaList_wszgds)
        if (spider.name == 'wszgcs'):
            self.urlList_wszgcs = self.templist_wszgcs
            # 将数据写入文件
            self.write_file("./jsonfile/wszgcs_UrlList.json", self.urlList_wszgcs)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgcs_DeltaList.json", self.deltaList_wszgcs)
        if (spider.name == 'wszgzh'):
            self.urlList_wszgzh = self.templist_wszgzh
            # 将数据写入文件
            self.write_file("./jsonfile/wszgzh_UrlList.json", self.urlList_wszgzh)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgzh_DeltaList.json", self.deltaList_wszgzh)
        if (spider.name == 'hhtjl'):
            self.urlList_hhtjl = self.templist_hhtjl
            # 将数据写入文件
            self.write_file("./jsonfile/hhtjl_UrlList.json", self.urlList_hhtjl)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtjl_DeltaList.json", self.deltaList_hhtjl)
        if (spider.name == 'hhtcs'):
            self.urlList_hhtcs = self.templist_hhtcs
            # 将数据写入文件
            self.write_file("./jsonfile/hhtcs_UrlList.json", self.urlList_hhtcs)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtcs_DeltaList.json", self.deltaList_hhtcs)
        if (spider.name == 'hhtxq'):
            self.urlList_hhtxq = self.templist_hhtxq
            # 将数据写入文件
            self.write_file("./jsonfile/hhtxq_UrlList.json", self.urlList_hhtxq)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtxq_DeltaList.json", self.deltaList_hhtxq)
        if (spider.name == 'hhtgz'):
            self.urlList_hhtgz = self.templist_hhtgz
            # 将数据写入文件
            self.write_file("./jsonfile/hhtgz_UrlList.json", self.urlList_hhtgz)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtgz_DeltaList.json", self.deltaList_hhtgz)
    def write_file(self,path,list):
        self.f = open(path, "w", encoding='UTF-8')
        content = json.dumps(list, ensure_ascii=False)
        self.f.write(content)
        self.f.close()
    def read_file(self,path):
        try:
            self.f = open(path, "r", encoding='UTF-8')  # 读取josn中的上次的链接
            return json.load(self.f)  # 将数据存入列表
        except:
            self.write_file(path,[])
    def Kafka_fun(self,item,origin):
        global producer
        
        dict = {'TITLE':'','INTRODUCTION':'','ORIGIN_VALUE':'','ORIGIN_NAME':'','OCCUR_TIME':'','URL':''}
        dict['TITLE']=item['title']
        dict['URL']=item['UrlId']
        dict['INTRODUCTION']=item['info']
        dict['OCCUR_TIME']=item['time']
        dict['ORIGIN_VALUE']='500010000000001'
        print("55555555555555555555555555555555555555"+origin)
        dict['ORIGIN_NAME']='论坛'
        #if(str(origin).startswith('hht')):
         #   dict['ORIGIN_NAME']='户户通'
        #elif(str(origin).startswith('jdwx')):
         #   dict['ORIGIN_NAME']='家电维修'
        #elif(str(origin).startswith('wszg')):
         #   dict['ORIGIN_NAME']='卫视中国'
        #elif(str(origin).startswith('sbaidu')):
         #   dict['ORIGIN_NAME']='百度论坛'
        msg = json.dumps(dict,ensure_ascii=False)
        print("------------------------------------------------------------------------------------"+msg)
        producer.send('test', msg.encode('utf-8'))
