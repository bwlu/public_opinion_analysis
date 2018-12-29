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

producer = KafkaProducer(bootstrap_servers=['192.168.163.184:6667'])

def GetgzhList(keyword, page):
    isSucess = False
    mostTryCounts = 3  # 最大尝试次数
    count = 0
    while (isSucess == False and count < mostTryCounts):
        count = count + 1
        iplist = read_Proxies()  # 得到代理IP列表
        itemList = []
        IP = {}
        ss = 0 # 成功的次数
        ff = 0 # 不成功的次数
        for ip in iplist:
            try:
                ws_api = wechatsogou.WechatSogouAPI(proxies=ip, timeout=5)
                itemList = get_data(ws_api.search_gzh(keyword, page=page), 1)  # 得到数据，并转换数据
                print("返回后公众号列表长度:" + str(len(itemList)))
                ss = ss+1
                if (len(itemList) != 0):
                    IP = ip
                    isSucess = True
                    break
            except Exception as e:
                print("公众号访问出错，检测ip是否失效")
                ff = ff+1
                print(e)
                check_ip(ip)
                continue
        if isSucess == False and ss <= ff:
            get_ip()
    if isSucess == False:
        print("ERROR" + " 可能关键字不存在或者已经爬到最后一页")
    else:
        print("SUCESS")
        return [itemList, IP, keyword]

# 检测ip是否失效
def check_ip(ips):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    # 以下测试IP
    try:
        requests.get("http://www.baidu.com", headers=headers, proxies=ips, timeout=2)  # 测试用网站
        print('停止2s.......................')
        time.sleep(2)
    except Exception as e:
        print("Ip已失效:",e)
        usefulIPlist = read_Proxies()[1:]
        writeProxies(usefulIPlist)

# 获取免费代理
def get_ip_free():
    print('===================获取免费代理ip===================')
    """ 从代理网站上获取代理"""
    url = 'http://www.xicidaili.com/wt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    ip_list = []
    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("请求ip失败：",e)
        return False
    soup = BeautifulSoup(page.text, 'lxml')
    ul_list = soup.find_all('tr', limit=15)  # limit=30
    print("IP池ip个数为：%d"%len(ul_list))
    for i in range(2, len(ul_list)):
        line = ul_list[i].find_all('td')
        ip = line[1].text
        port = line[2].text
        address = ip + ':' + port
        proxy = get_proxy(address)
        ip_list.append(proxy)
    # 以下测试IP
    usefulIPlist = []
    for ip in ip_list:
        try:
            page = requests.get("http://www.baidu.com", headers=headers, proxies=ip, timeout=2)  # 测试用网站
            print("ip可用")
            usefulIPlist.append(ip)
        except:
            print("Ip不可用")
    if (len(usefulIPlist) == 0):
        print("ip获取失败")
        get_ip_free()
    else:
        print("可用ip个数为：%d"%len(usefulIPlist))
        ratio = len(usefulIPlist)/15
        print('==========================ip可用率:%s'%str(ratio))
        writeProxies(usefulIPlist)
    return True

# 获取付费代理
def get_ip():
    with open('wechatatricles_ipipip.txt','a+') as fp:
        fp.write('获取ip\n')
    """ 从代理网站上获取代理"""
    print('===================获取付费代理ip===================')
    url = 'https://proxy.horocn.com/api/proxies?order_id=902H1620817998792613&num=5&format=jsons&line_separator=unix'
    url = 'http://webapi.http.zhimacangku.com/getip?num=5&type=1&pro=&city=0&yys=0&port=1&pack=37981&ts=0&ys=0&cs=0&lb=1&sb=0&pb=5&mr=2&regions='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    ip_list = []
    try:
        zm_resp = requests.get(url)
        ip_json = zm_resp.text.split('\r\n')
        if len(ip_json)==1:
            print('===================付费代理ip已达上限===================')
            print(ip_json[0])
            get_ip_free()
            return True
    except Exception as e:
        print("请求ip失败:",e)
        get_ip()
        return False
    print("IP池ip个数为：%d"%(len(ip_json)-1))
    for ip in ip_json:
        # host = ips['host']
        # port = ips['port']
        # ip = '%s:%s'%(host,port)
        if ip != "":
            proxy = get_proxy(ip)
            # print(proxy)
            ip_list.append(proxy)
    # 以下测试IP
    usefulIPlist = []
    for ip in ip_list:
        try:
            page = requests.get("http://www.baidu.com", headers=headers, proxies=ip, timeout=2)  # 测试用网站
            print("ip可用：%s"%ip)
            usefulIPlist.append(ip)
        except Exception as e:
            print("Ip不可用:",e)
            # print("Ip不可用")
    if (len(usefulIPlist) == 0):
        print("ip获取失败,重新获取")
        get_ip()
    else:
        print("可用ip个数为：%d"%len(usefulIPlist))
        ratio = len(usefulIPlist)/20
        print('==========================ip可用率:%s'%str(ratio))
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
    except Exception as e:
        print("文件不存在")
        print(e)
        return []

def get_data(listDic, mode):  # 1公众号列表 2文章列表
    print("获取列表长度:" + str(len(listDic)))
    itemList = []
    if mode == 1:
        for dic in listDic:
            gzh = dic['wechat_name']
            # gzh = dic['profile_url']
            itemList.append(gzh)
    if mode == 2:
        listArticle = listDic['article']
        for art in listArticle:
            localtime = time.localtime(art['datetime'])
            t = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            dic = {
                'title': art['title'],
                'info': art['abstract'],
                'time': t,
                'url': art['content_url']
            }
            itemList.append(dic)
    return itemList


def get_article(gzh):
    articleList = []
    deltaList = []
    maxConut = 3
    titleList = read_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou.json")
    keyword = gzh
    count = 0
    isSuccess = False
    with open('wechatatricles_zhima.txt','a+') as fp:
        fp.write('公众号：%s===============\n'%gzh)
        log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fp.write('time:%s\n'%log_time)
    while (1):
        iplist = read_Proxies()
        print('读取ip============================================')
        for ip in iplist:
            try:
                ws_api = wechatsogou.WechatSogouAPI(proxies=ip, timeout=10)
                itemList = get_data(ws_api.get_gzh_article_by_history(keyword), 2)  # 得到数据，并转换数据
                print("\n返回后文章列表长度:" + str(len(itemList)))
                with open('wechatatricles_zhima.txt','a+') as fp:
                    fp.write('文章*************************%d\n'%len(itemList))
                    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    fp.write('time:%s\n'%log_time)
                for art in itemList:
                    print(art['title'])
                    articleList.append(art)  # 存入文章列表
                    if art['title'] not in titleList:
                        #
                        # 增量,在此处存入消息队列
                        Kafka_fun(art)
                        #
                        deltaList.append(art['title'])
                print("下一组文章")
                isSuccess = True
                break
            except Exception as e:
                with open('wechatatricles_zhima.txt','a+') as fp:
                    fp.write('00000000000000000000000000000000000000\n')
                    fp.write('文章访问出错\n')
                    fp.write('%s\n'%str(e))
                    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    fp.write('time:%s\n'%log_time)
                print("文章访问出错,检测ip是否失效")
                print(e)
                check_ip(ip)
                continue
        if (isSuccess == False):
            count = count + 1
            if (count > maxConut):
                with open('wechatatricles_zhima.txt','a+') as fp:
                    fp.write('11111111111111111111111111111111111111111\n')
                    fp.write('尽力了，文章被封锁了！\n')
                    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    fp.write('time:%s\n'%log_time)
                print("尽力了，文章被封锁了！")  # 封锁后直接返回已爬取的
                return False
            else:
                get_ip()  # 得到代理IP列表
                continue
        else:
            break
    print("Finish")
    with open('wechatatricles_zhima.txt','a+') as fp:
        fp.write('*************************\n')
        fp.write('Finish\n')
        fp.write('\n\n')
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
    #producer = KafkaProducer(bootstrap_servers=['192.168.163.184:6667'])
    title_list = []  # 最终的文章列表
    if len(read_Proxies())==0:
        if (get_ip() == False):
            print("无法获得代理")
            return

    testlist = [{'title': '1', 'info': '11', 'time': '1', 'url': '1'},  # 测试用数据
                {'title': '2', 'info': '22', 'time': '1', 'url': '1'},
                {'title': '3', 'info': '33', 'time': '1', 'url': '1'},
                {'title': '4', 'info': '44', 'time': '1', 'url': '1'},
                {'title': '5', 'info': '55', 'time': '1', 'url': '1'}]
    keylist = getKeylist()
    # gzhList = []
    for key in keylist:
        # 处理公众号
        page = 1
        isEnd = False  # 判断是否爬到尾页
        while (1):
            gzhList = []
            print("公众号%s=====================第%d页"%(key,page))
            tempList = GetgzhList(key, page)  # 得到公众号列表
            try:
                testList = tempList[0]  # 用来判断是否为空
            except:
                isEnd = True
                break
            for gzh in tempList[0]:
                print(gzh)
                if (gzh != None):
                    gzhList.append(gzh)
            page = page + 1
            if (isEnd == True): break
            # #################################
            pageCount = 0
            for gzh in gzhList:
                print(gzh)
                pageCount = pageCount+1
                #获得公众号文章
                print('关键词：%s,爬取公众号====%s====文章，第%d页，第%d个'%(key,gzh,page-1,pageCount))
                article_list = get_article(gzh)
                if(article_list==False):
                    print('失败停止停止5s=============================================')
                    time.sleep(5)#失败停止5s
                    continue
                else:
                    for article in article_list:  # 将文章存入titlelist
                        title_list.append(article['title'])
                    write_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou.json", title_list)
    write_file("./baiduspiderProject_new/baiduspider/jsonfile/sougou.json", title_list)

def write_file(path, list):
    f = open(path, "w", encoding='UTF-8')
    content = json.dumps(list, ensure_ascii=False)
    f.write(content)
    f.close()

def read_file(path):
    try:
        f = open(path, "r", encoding='UTF-8')  # 读取josn中的上次的链接
        return json.load(f)  # 将数据存入列表
    except:
        return []

def Kafka_fun(art):
    global producer
    dict = {'TITLE': '', 'INTRODUCTION': '', 'ORIGIN_VALUE': '', 'ORIGIN_NAME': '', 'OCCUR_TIME': '', 'URL': ''}
    dict['TITLE'] = art['title'][:50]
    dict['URL'] = art['url']
    dict['INTRODUCTION'] = art['info'][:400]
    # localtime = time.localtime()
    # t = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    dict['OCCUR_TIME'] = art['time']
    dict['ORIGIN_VALUE'] = '500010000000002'
    dict['ORIGIN_NAME'] = '微信'

    msg = json.dumps(dict, ensure_ascii=False)
    print("------------------------------------------------------------------------------------")
    # print(msg)
    producer.send('postsarticles', msg.encode('utf-8'))


# 以下为运行所用代码
run()
