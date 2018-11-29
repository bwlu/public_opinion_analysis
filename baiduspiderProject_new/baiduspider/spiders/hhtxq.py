# -*- coding: utf-8 -*-
import scrapy
import datetime
from baiduspider.items import BaiduspiderItem


class hhtxqSpider(scrapy.Spider):
    name = 'hhtxq'
    allowed_domains = ['www.huhutong315.com']
    start_urls = ["http://www.huhutong315.com/forum-92-1.html"
                  ]
    default_scope_day = 365  # 爬取时限(日)
    allowed_timesup = 10  # 最多超过时限次数
    def parse(self, response):
        nodelist = response.xpath('//tbody/tr/th')#得到一页中的所有帖子
        item = BaiduspiderItem()
        isHasContent = False  # 判断此页中是否有合适的信息
        NextPageUrl = ''
        timecount = 0  # 计数器
        for node in nodelist:#分析帖子信息
            item["title"]= node.xpath("./a[2][@class='s xst']/text()").extract_first()
            item["UrlId"] = node.xpath("./a[2][@class='s xst']/@href").extract_first()
            item["info"] = node.xpath("./em/a/text()").extract_first()
            item["time"] = node.xpath('./a[2]/../../td[@class="by"]/em/span/text()').extract_first()

            # 处理时间为空的情况
            if item["time"] == None:
                item["time"] = ''
            else:
                item["time"] = item["time"].strip()
            # 处理简介为空的情况
            if item["info"] == None:
                item["info"] = ''
            # 判断这个帖子是否符合时间
            if(self.TimeMarch(item["time"])==True):
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
            print("翻页了！！！！！！！！！！！！！！！！！")


    def TimeMarch(self,dataT):
        IsLimitedLable = False  # 判断是否超过默认年限

        if(dataT.count('-')<1): # 如果是秒时分或几天内
            return True
        else:
            splits = dataT.split("-")

            if (int(splits[0]) < 13):  # 其他
                IsLimitedLable = True
                return IsLimitedLable
            else:
                time = datetime.datetime(int(splits[0]), int(splits[1]), int(splits[2]))
                deltatime = (datetime.datetime.now() - time).days
                if(deltatime<self.default_scope_day):#如果时限小于一年
                    IsLimitedLable = True
                    return IsLimitedLable
                else:#时限大于一年的话
                    return IsLimitedLable










