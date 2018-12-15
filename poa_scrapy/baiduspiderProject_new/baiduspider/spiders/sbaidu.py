# -*- coding: utf-8 -*-
import scrapy
from .. import read_json
import datetime
import os
from oraclepool import OrclPool
from baiduspider.items import BaiduspiderItem
from .. import TimeCalculate
from .. import TimeMarch


class SimpleBaiduSpider(scrapy.Spider):
    name = 'sbaidu'
    allowed_domains = ['tieba.baidu.com']
    if(read_json.read_json(name)):
        default_scope_day = 50 #首次爬取时限
    else:
        default_scope_day = 30 #增量爬取时限
	
	#取得关键字
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
    keylist=list(keylist)
    urlList = []
    for key in keylist:
        urlList.append('https://tieba.baidu.com/f?kw=' + str(key))
    # 将拼接好的字符串加入初始url
    start_urls = urlList


    def parse(self, response):
        nodelist = response.xpath('//div[@class="col2_right j_threadlist_li_right "]')#得到一页中的所有帖子
        item = BaiduspiderItem()
        isHasContent = False  # 判断此页中是否有合适的信息
        NextPageUrl = ''
        for node in nodelist:#分析帖子信息
            item["title"]= node.xpath("./div[1]/div/a[@title]/text()").extract_first()
            item["UrlId"] = node.xpath("./div[1]/div/a[@href]/@href").extract_first()
            item["info"] = node.xpath('./div[2]/div[@class="threadlist_text pull_left"]/div[1]/text()').extract_first()
            item["time"] = node.xpath('./div[1]/div[2]/span[@title="创建时间"]/text()').extract_first()
            item["time"] = item["time"] = TimeCalculate.time_calculate(item["time"], self.name)
            # 判断一页中是否有符合年限的帖子
            if(isHasContent == False):
                isHasContent = TimeMarch.time_March(item["time"],self.default_scope_day)
            # 判断这个帖子是否符合时间
            if(TimeMarch.time_March(item["time"],self.default_scope_day)==True):
                item["IsLimitedTime"] = 'y'
            else:
                item["IsLimitedTime"] = 'n'
            # 拼接子url
            childUrl = "https://tieba.baidu.com" + item["UrlId"]
            item["UrlId"] = childUrl
            # 处理简介为空的情况
            if item["info"] == None:
                item["info"]= ''
            else:
                item["info"]=item["info"].strip()#将多余空格去掉
            item["time"] = item["time"].strip()
            if(NextPageUrl == ''):#记录下一页的链接
                NextPageUrl = 'https:'+ response.xpath('//a[@class = "next pagination-item "]/@href').extract_first()

            yield item #返回数据到pipeline
        if(isHasContent==False):#根据判断决定继续爬取还是结束
             self.crawler.engine.close_spider(self, 'Finished')#关闭爬虫
        else:
            yield scrapy.Request(NextPageUrl,callback = self.parse)











