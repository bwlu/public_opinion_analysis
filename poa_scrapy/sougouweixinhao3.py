# -*- coding: utf-8 -*-

import wechatsogou
import requests
import random
import time
import json
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import os
from oraclepool import OrclPool

global producer
def GetgzhList(keyword):
    isSucess=False
    mostTryCounts=20 #最大尝试次数
    count=0
    while(isSucess==False and count<mostTryCounts):
        count = count +1
        iplist  = read_Proxies()#得到代理IP列表
        itemList = []
        IP={}
        for ip in iplist:
            try:
                ws_api = wechatsogou.WechatSogouAPI(proxies=ip,timeout=20)

                itemList =get_data(ws_api.search_gzh(keyword),1)#得到数据，并转换数据
                print("返回后列表长度:"+ str(len(itemList)))
                if(len(itemList)!=0):
                    IP = ip
                    isSucess=True
                    break
            except:
                print("访问出错")
                continue
    if(isSucess==False):
        print("ERROR"+" 可能关键字不存在")

    else:
        print("SUCESS")
        return [itemList,IP,keyword]
#被弃用IP
def get_ip():
    """ 从代理网站上获取代理"""
    url = 'http://www.xicidaili.com/wt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    ip_list = []
    try:
        page = requests.get(url, headers=headers)
    except:
        print("请求ip失败")
        return False
    soup = BeautifulSoup(page.text, 'lxml')
    ul_list = soup.find_all('tr', limit=30)#limit=30
    print("IP池ip个数为："+ str(len(ul_list)))
    for i in range(2, len(ul_list)):
        line = ul_list[i].find_all('td')
        ip = line[1].text
        port = line[2].text
        address = ip + ':' + port
        proxy = get_proxy(address)
        ip_list.append(proxy)
    #以下测试IP
    usefulIPlist = []

    for ip in ip_list:
        try:
            page = requests.get("http://www.baidu.com", headers=headers, proxies=ip,timeout=2)  # 测试用网站
            print("ip可用")
            usefulIPlist.append(ip)
        except:
            print("Ip不可用")
    if(len(usefulIPlist)==0) :
        print("ip获取失败")
        writeProxies([])
    else:
        print("IP可用")
        writeProxies(usefulIPlist)
    return True
def get_proxy(aip):
    """构建格式化的单个proxies"""
    proxy_ip = 'http://' + aip
    proxy_ips = 'https://' + aip
    proxy = {"http": proxy_ip, "https": proxy_ips}
    return proxy
def writeProxies(proxies):
    f = open("proxies.json", "w", encoding='UTF-8')
    content = json.dumps(proxies, ensure_ascii=False)
    f.write(content)
    print("写入完成")
    f.close()
def read_Proxies():
    try:
        f = open('proxies.json', "r", encoding='UTF-8')  # 读取josn中的上次的链接
        return json.load(f)  # 将数据存入列表
    except:
        print("文件不存在")
        return []

def get_data(listDic,mode):#1公众号列表 2文章列表
    print("获取列表长度:"+str(len(listDic)))
    itemList = []
    if mode == 1:
        for dic in listDic:
            gzh = dic['wechat_name']
            itemList.append(gzh)
    if mode == 2:
        listArticle = listDic['article']
        for art in listArticle:
            Kafka_fun(art)
            localtime =time.localtime(art['datetime'])
            t = time.strftime("%Y-%m-%d %H:%M:%S",localtime)
            dic = {
                'title': art['title'],
                'info': art['abstract'],
                'time': t,
                'url': art['content_url']
            }
            itemList.append(dic)
    return itemList

def get_article(gzhList,ip):
    articleList = []
    iplist = read_Proxies()
    deltaList = []
    maxConut=1
    titleList = read_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou.json")
    for gzh in gzhList:
        keyword = gzh
        count=0
        isSuccess= False
        while(1):
            for ip in iplist:
                try:
                    ws_api = wechatsogou.WechatSogouAPI(proxies=ip, timeout=10)
                    itemList = get_data(ws_api.get_gzh_article_by_history(keyword), 2)  # 得到数据，并转换数据
                    print("返回后文章列表长度:" + str(len(itemList)))
                    for art in itemList:
                        print(art)
                        articleList.append(art)#存入文章列表
                        if art['title'] not in titleList:
                            #
                            # 增量,在此处存入消息队列
                            #
                            deltaList.append(art['title'])
                    print("下一组文章")
                    isSuccess =True
                    break
                except:
                    print("文章访问出错")
                    continue
            if(isSuccess==False):
                count = count + 1
                if (count > maxConut):
                    print("尽力了，文章被封锁了！")  # 封锁后直接返回已爬取的
                    write_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou_delta.json", deltaList)
                    return articleList
                else:
                    get_ip()  # 得到代理IP列表
                    continue
            else:
                break
    write_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou_delta.json", deltaList)
    print("Finish")
    return articleList

def getKeylist():
    # 取得关键字
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    op = OrclPool()
    sql = "select key_word from BASE_ANALYSIS_SENTIMENT where DICT_ENABLED_VALUE=300010000000001"
    list1 = op.fetch_all(sql)
    keylist = []
    for node in list1:
        temp1 = str(node).replace("'", '')
        temp2 = temp1.replace("(" or ")", "")
        temp3 = temp2.replace(")", "")
        temp4 = temp3.split(",")
        for key in temp4:
            if key != '':
                keylist.append(key)
    keylist = set(keylist)
    keylist = list(keylist)
    return keylist


def run():
    global producer
    producer = KafkaProducer(bootstrap_servers=['192.168.163.184:6667'])
    title_list = []#最终的文章列表
    if(get_ip()==False):
        print("无法获得代理")
        return

    testlist=[{'title': '1', 'info': '11', 'time': '1', 'url': '1'},#测试用数据
              {'title': '2', 'info': '22', 'time': '1', 'url': '1'},
              {'title': '3', 'info': '33', 'time': '1', 'url': '1'},
              {'title': '4', 'info': '44', 'time': '1', 'url': '1'},
              {'title': '5', 'info': '55', 'time': '1', 'url': '1'}]
    keylist = getKeylist()
    keylist = ['杨主任','户户通']
    for key in keylist:
        tempList=GetgzhList(key)#得到公众号列表
        gzhList = tempList[0]
        for gzh in gzhList:
            print(gzh)
        ip = tempList[1]
        article_list = get_article(gzhList,ip)
        for article in article_list:#将文章存入titlelist
            title_list.append(article['title'])

    write_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou.json",title_list)

def write_file(path,list):
        f = open(path, "w", encoding='UTF-8')
        content = json.dumps(list, ensure_ascii=False)
        f.write(content)
        f.close()
def read_file(path):
        try:
            f = open(path, "r", encoding='UTF-8')  # 读取josn中的上次的链接
            return json.load(f)  # 将数据存入列表
        except:
            write_file(path,[])
			
def Kafka_fun(art):
        global producer
        
        dict = {'TITLE':'','INTRODUCTION':'','ORIGIN_VALUE':'','ORIGIN_NAME':'','OCCUR_TIME':'','URL':''}
        dict['TITLE']=art['title']
        dict['URL']=art['cover']
        dict['INTRODUCTION']=art['abstract']
        localtime = time.localtime(art['datetime'])
        t = time.strftime("%Y-%m-%d %H:%M:%S",localtime)
        dict['OCCUR_TIME']=t
        dict['ORIGIN_VALUE']='500010000000002'
        dict['ORIGIN_NAME']='微信'
        
        msg = json.dumps(dict,ensure_ascii=False)
        print("------------------------------------------------------------------------------------"+msg)
        producer.send('postsarticles', msg.encode('utf-8'))

			
#以下为运行所用代码
run()
