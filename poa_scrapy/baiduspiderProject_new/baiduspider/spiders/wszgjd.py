# -*- coding: utf-8 -*-
import scrapy
import datetime
from .. import TimeCalculate
from .. import TimeMarch
from .. import ChildPage
from baiduspider.items import BaiduspiderItem
from .. import read_json

class wsjgjdSpider(scrapy.Spider):
    name = 'wszgjd'
    allowed_domains = ['www.wszgw.net']
    start_urls = ['https://www.wszgw.net/forum-284-1.html',
                  'https://www.wszgw.net/forum-285-1.html',
                  'https://www.wszgw.net/forum-286-1.html',
                  'https://www.wszgw.net/forum-287-1.html',
                  'https://www.wszgw.net/forum-288-1.html',
                  'https://www.wszgw.net/forum-289-1.html',
                  'https://www.wszgw.net/forum-290-1.html',
                  'https://www.wszgw.net/forum-291-1.html',
                  ]
    allowed_timesup = 10  # 最多超过时限次数
    if(read_json.read_json(name)):
        default_scope_day = 50 #首次爬取时限
    else:
        default_scope_day = 30 #增量爬取时限


    def parse(self, response):
        nodelist = response.xpath('//tbody/tr/th')#得到一页中的所有帖子
        item = BaiduspiderItem()
        isHasContent = False  # 判断此页中是否有合适的信息
        NextPageUrl = ''
        timecount = 0  # 计数器
        for node in nodelist:#分析帖子信息
            item["title"]= node.xpath("./a[2][@class='s xst']/text()").extract_first()
            childUrl = node.xpath("./a[2][@class='s xst']/@href").extract_first()
            item["UrlId"] = node.xpath("./a[2][@class='s xst']/@href").extract_first()
            if (childUrl != None):
                item["info"] = ChildPage.ChildPage(childUrl, '3')
            item["time"] = node.xpath('./a[2]/../../td[@class="by"]/em/span/text()').extract_first()

            # 处理时间为空的情况
            if item["time"] == None:
                item["time"] = ''
            else:
                item["time"] = item["time"].strip()
                item["time"] = TimeCalculate.time_calculate(item["time"], self.name)
            # 处理简介为空的情况
            # if item["info"] == None:
            #     item["info"] = ''
            # 判断这个帖子是否符合时间
            if (TimeMarch.time_March(item["time"], self.default_scope_day) == True):
                item["IsLimitedTime"] = 'y'
            else:
                item["IsLimitedTime"] = 'n'
                timecount = timecount + 1


            if(NextPageUrl == ''):#记录下一页的链接
                NextPageUrl =response.xpath('//a[@class="bm_h"]/@rel').extract_first()
            if item["UrlId"] != None:  # 非普通帖子的错误处理（置顶帖等异常的帖子）
                yield item #返回数据到pipeline
        if(timecount>self.allowed_timesup or NextPageUrl==None):#根据判断决定继续爬取还是结束
            #结束爬取
            item = BaiduspiderItem()
            item["IsLimitedTime"]='n'
            yield item
        else:
            yield scrapy.Request('https://www.wszgw.net/'+NextPageUrl,callback = self.parse)









