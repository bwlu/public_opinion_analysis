import time
import json
import os
from kafka import KafkaProducer   #引入包，如果你在自己的电脑上跑，得先安装kafka
global producer
class BaiduspiderPipeline(object):
#百度列表
    urlList_baidu = []
    deltaList_baidu=[]
    templist_baidu = []
    informList_baidu = []
#家电维修供求部分列表
    urlList_jdwxgq = []
    deltaList_jdwxgq = []
    templist_jdwxgq = []
    informList_jdwxgq = []
#家电维修表彰部分列表
    urlList_jdwxbz = []
    deltaList_jdwxbz = []
    templist_jdwxbz = []
    informList_jdwxbz = []
#家电维修投诉部分列表
    urlList_jdwxts = []
    deltaList_jdwxts = []
    templist_jdwxts = []
    informList_jdwxts = []
# 家电维修公告部分列表
    urlList_jdwxgg = []
    deltaList_jdwxgg = []
    templist_jdwxgg = []
    informList_jdwxgg = []
# 卫视中国家电列表
    urlList_wszgjd = []
    deltaList_wszgjd = []
    templist_wszgjd = []
    informList_wszgjd = []
# 卫视中国电视列表
    urlList_wszgds = []
    deltaList_wszgds = []
    templist_wszgds = []
    informList_wszgds = []
# 卫视中国参数直通车列表
    urlList_wszgcs = []
    deltaList_wszgcs = []
    templist_wszgcs = []
    informList_wszgcs = []
# 卫视中国综合列表
    urlList_wszgzh = []
    deltaList_wszgzh = []
    templist_wszgzh = []
    informList_wszgzh = []
# 户户通交流列表
    urlList_hhtjl = []
    deltaList_hhtjl = []
    templist_hhtjl = []
    informList_hhtjl = []
# 户户通测试列表
    urlList_hhtcs = []
    deltaList_hhtcs = []
    templist_hhtcs = []
    informList_hhtcs = []
# 户户通需求列表
    urlList_hhtxq = []
    deltaList_hhtxq = []
    templist_hhtxq = []
    informList_hhtxq = []
# 户户通故障列表
    urlList_hhtgz = []
    deltaList_hhtgz = []
    templist_hhtgz = []
    informList_hhtgz = []
    def __init__(self):
        global producer
        producer = KafkaProducer(bootstrap_servers=['172.16.54.139:6667'])
  
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
                id = item['UrlId'].split('/')[4]#得到urlid
                self.templist_baidu.append(id)
                #比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[4]
                try:
                    if id not in self.urlList_baidu:
                        self.deltaList_baidu.append(id)
                        self.informList_baidu.append(dict(item))
                except:
                    self.deltaList_baidu.append(id)
                    self.informList_baidu.append(dict(item))
        if(spider.name == 'jdwxgq'):
            if (item["IsLimitedTime"] == "y"):
               
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_jdwxgq.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:#首次添加的异常处理
                    if num not in self.urlList_jdwxgq:
                        self.deltaList_jdwxgq.append(num)
                        self.informList_jdwxgq.append(dict(item))
                except:
                    self.deltaList_jdwxgq.append(num)
                    self.informList_jdwxgq.append(dict(item))
        if(spider.name == 'jdwxbz'):
            if (item["IsLimitedTime"] == "y" and item['UrlId'] != None):
               
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_jdwxbz.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:#首次添加的异常处理
                    if num not in self.urlList_jdwxbz:
                        self.deltaList_jdwxbz.append(num)
                        self.informList_jdwxbz.append(dict(item))
                except:
                    self.deltaList_jdwxbz.append(num)
                    self.informList_jdwxbz.append(dict(item))
        if(spider.name == 'jdwxts'):
            if (item["IsLimitedTime"] == "y"):
               
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_jdwxts.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:#首次添加的异常处理
                    if num not in self.urlList_jdwxts:
                        self.deltaList_jdwxts.append(num)
                        self.informList_jdwxts.append(dict(item))
                except:
                    self.deltaList_jdwxts.append(num)
                    self.informList_jdwxts.append(dict(item))
        if(spider.name == 'jdwxgg'):
            if (item["IsLimitedTime"] == "y"):
              
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_jdwxgg.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_jdwxgg:
                        self.deltaList_jdwxgg.append(num)
                        self.informList_jdwxgg.append(dict(item))
                except:
                    self.deltaList_jdwxgg.append(num)
                    self.informList_jdwxgg.append(dict(item))
        if(spider.name == 'wszgjd'):
            if (item["IsLimitedTime"] == "y"):
                
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_wszgjd.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgjd:
                        self.deltaList_wszgjd.append(num)
                        self.informList_wszgjd.append(dict(item))
                except:
                    self.deltaList_wszgjd.append(num)
                    self.informList_wszgjd.append(dict(item))
        if(spider.name == 'wszgds'):
            if (item["IsLimitedTime"] == "y"):
                
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_wszgds.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgds:
                        self.deltaList_wszgds.append(num)
                        self.informList_wszgds.append(dict(item))
                except:
                    self.deltaList_wszgds.append(num)
                    self.informList_wszgds.append(dict(item))
        if(spider.name == 'wszgcs'):
            if (item["IsLimitedTime"] == "y"):
               
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_wszgcs.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgcs:
                        self.deltaList_wszgcs.append(num)
                        self.informList_wszgcs.append(dict(item))
                except:
                    self.deltaList_wszgcs.append(num)
                    self.informList_wszgcs.append(dict(item))
        if(spider.name == 'wszgzh'):
            if (item["IsLimitedTime"] == "y"):
                
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_wszgzh.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_wszgzh:
                        self.deltaList_wszgzh.append(num)
                        self.informList_wszgzh.append(dict(item))
                except:
                    self.deltaList_wszgzh.append(num)
                    self.informList_wszgzh.append(dict(item))
        if (spider.name == 'hhtjl'):
            if (item["IsLimitedTime"] == "y"):
              
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_hhtjl.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtjl:
                        self.deltaList_hhtjl.append(num)
                        self.informList_hhtjl.append(dict(item))
                except:
                    self.deltaList_hhtjl.append(num)
                    self.informList_hhtjl.append(dict(item))
        if (spider.name == 'hhtcs'):
            if (item["IsLimitedTime"] == "y"):
                
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_hhtcs.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtcs:
                        self.deltaList_hhtcs.append(num)
                        self.informList_hhtcs.append(dict(item))
                except:
                    self.deltaList_hhtcs.append(num)
                    self.informList_hhtcs.append(dict(item))
        if (spider.name == 'hhtxq'):
            if (item["IsLimitedTime"] == "y"):
                
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_hhtxq.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtxq:
                        self.deltaList_hhtxq.append(num)
                        self.informList_hhtxq.append(dict(item))
                except:
                    self.deltaList_hhtxq.append(num)
                    self.informList_hhtxq.append(dict(item))
        if (spider.name == 'hhtgz'):
            if (item["IsLimitedTime"] == "y"):
               
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                self.templist_hhtgz.append(num)
                # 比对id找到增量，并存入Kafka
                id = item['UrlId'].split('/')[3]  # 得到urlid
                num = id.split('-')[1]
                try:  # 首次添加的异常处理
                    if num not in self.urlList_hhtgz:
                        self.deltaList_hhtgz.append(num)
                        self.informList_hhtgz.append(dict(item))
                except:
                    self.deltaList_hhtgz.append(num)
                    self.informList_hhtgz.append(dict(item))
        return item
    def close_spider(self,spider):
        if(spider.name =='sbaidu'):
            self.urlList_baidu = self.templist_baidu
            #将数据写入文件
            #self.write_file("./jsonfile/baidu_UrlList.json",self.urlList_baidu)
            self.chengeUrlListFile(self.urlList_baidu,spider.name)
            #将差值列表存入josn
            self.write_file("./jsonfile/baidu_DeltaList.json",self.deltaList_baidu)
            #关闭爬虫时将数据写入消息队列
            self.kafka_input(self.informList_baidu,spider.name)
        if(spider.name == 'jdwxgq'):
            self.urlList_jdwxgq = self.templist_jdwxgq
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_jdwxgq, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxgq_DeltaList.json", self.deltaList_jdwxgq)
            self.kafka_input(self.informList_jdwxgq, spider.name)
        if(spider.name == 'jdwxbz'):
            self.urlList_jdwxbz = self.templist_jdwxbz
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_jdwxbz, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxbz_DeltaList.json", self.deltaList_jdwxbz)
            self.kafka_input(self.informList_jdwxbz, spider.name)
        if(spider.name == 'jdwxts'):
            self.urlList_jdwxts = self.templist_jdwxts
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_jdwxts, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxts_DeltaList.json", self.deltaList_jdwxts)
            self.kafka_input(self.informList_jdwxts, spider.name)
        if(spider.name == 'jdwxgg'):
            self.urlList_jdwxgg = self.templist_jdwxgg
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_jdwxgg, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/jdwxgg_DeltaList.json", self.deltaList_jdwxgg)
            self.kafka_input(self.informList_jdwxgg, spider.name)
        if(spider.name == 'wszgjd'):
            self.urlList_wszgjd = self.templist_wszgjd
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_wszgjd, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgjd_DeltaList.json", self.deltaList_wszgjd)
            self.kafka_input(self.informList_wszgjd, spider.name)
        if(spider.name == 'wszgds'):
            self.urlList_wszgds = self.templist_wszgds
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_wszgds, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgds_DeltaList.json", self.deltaList_wszgds)
            self.kafka_input(self.informList_wszgds, spider.name)
        if (spider.name == 'wszgcs'):
            self.urlList_wszgcs = self.templist_wszgcs
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_wszgcs, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgcs_DeltaList.json", self.deltaList_wszgcs)
            self.kafka_input(self.informList_wszgcs, spider.name)
        if (spider.name == 'wszgzh'):
            self.urlList_wszgzh = self.templist_wszgzh
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_wszgzh, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/wszgzh_DeltaList.json", self.deltaList_wszgzh)
            self.kafka_input(self.informList_wszgzh, spider.name)
        if (spider.name == 'hhtjl'):
            self.urlList_hhtjl = self.templist_hhtjl
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_hhtjl, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtjl_DeltaList.json", self.deltaList_hhtjl)
            self.kafka_input(self.informList_hhtjl, spider.name)
        if (spider.name == 'hhtcs'):
            self.urlList_hhtcs = self.templist_hhtcs
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_hhtcs, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtcs_DeltaList.json", self.deltaList_hhtcs)
            self.kafka_input(self.informList_hhtcs, spider.name)
        if (spider.name == 'hhtxq'):
            self.urlList_hhtxq = self.templist_hhtxq
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_hhtxq, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtxq_DeltaList.json", self.deltaList_hhtxq)
            self.kafka_input(self.informList_hhtxq, spider.name)
        if (spider.name == 'hhtgz'):
            self.urlList_hhtgz = self.templist_hhtgz
            # 将数据写入文件
            self.chengeUrlListFile(self.urlList_hhtgz, spider.name)
            # 将差值列表存入josn
            self.write_file("./jsonfile/hhtgz_DeltaList.json", self.deltaList_hhtgz)
            self.kafka_input(self.informList_hhtgz, spider.name)
    def write_file(self,path,list):
        self.f = open(path, "w", encoding='UTF-8')
        content = json.dumps(list, ensure_ascii=False)
        self.f.write(content)
        self.f.close()
    def read_file(self,path):
        try:
            self.f = open(path, "r", encoding='UTF-8')  # 读取josn中的上次的链接
            content = json.load(self.f)
            self.f.close()
            return content   # 将数据存入列表
        except:
            self.write_file(path,[])
    def Kafka_fun(self,item,origin):
        global producer
        try:
            dict = {'TITLE':'','INTRODUCTION':'','ORIGIN_VALUE':'','ORIGIN_NAME':'','OCCUR_TIME':'','URL':''}
            dict['TITLE']=item['title'][:50]
            dict['URL']=item['UrlId']
            dict['INTRODUCTION']=item['info'][:400]
            dict['OCCUR_TIME']=item['time']
            dict['ORIGIN_VALUE']='500010000000001'
            dict['ORIGIN_NAME']='论坛'
            msg = json.dumps(dict,ensure_ascii=False)
            print('========================================')
            print(msg)
            producer.send('postsarticles', msg.encode('utf-8'))
        except Exception as e:
            self.export_log({"type":"producer","data":dict,"exception":str(e)})

    def export_log(log_info):
        log_time = time.strftime("%Y-%m-%d", time.localtime())
        log_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if not os.path.exists('/tmp/log/log_poa/'):
            os.makedirs('/tmp/log/log_poa/')
        with open('/tmp/log/log_poa/kafka-%s.log'%log_time,'a+') as fp:
            fp.write('%s:%s'%(log_time1,json.dumps(log_info,ensure_ascii=False)))
            fp.write('\n')
    def kafka_input(self,infoList,origin):
        if infoList != []:
            for info in infoList:
                self.Kafka_fun(info, origin)
        else:
            print("列表为空")
    def chengeUrlListFile(self,newlist,spidrName):
        if spidrName == 'sbaidu':
            fileList = self.read_file("./jsonfile/baidu_UrlList.json")
        else:
            fileList = self.read_file("./jsonfile/"+spidrName+"_UrlList.json")
        for num in newlist:
            if num not in fileList:
                fileList.append(num)
        if len(fileList)>1000:
            fileList = fileList[:200]
        if spidrName == 'sbaidu':
            self.write_file("./jsonfile/baidu_UrlList.json", fileList)
        else:
            self.write_file("./jsonfile/"+spidrName+"_UrlList.json", fileList)