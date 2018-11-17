# -*- coding: utf-8 -*-
import scrapy
import datetime
from baiduspider.items import BaiduspiderItem


class SimpleBaiduSpider(scrapy.Spider):
    name = 'sbaidu'
    content = '户户通'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw='+content]
    default_scope = 1 #爬取时限



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
            if(isHasContent == False):#判断一页中是否有符合年限的帖子
                isHasContent = self.TimeMarch(item["time"])

            childUrl = "https://tieba.baidu.com" + item["UrlId"]#拼接子url
            item["UrlId"] = childUrl
            if item["info"] == None:#处理简介为空的情况
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
            print("翻页了！！！！！！！！！！！！！！！！！")


    def TimeMarch(self,dataT):
        IsLimitedLable = False  # 判断是否超过默认年限
        splits = dataT.split("-")
        if (len(splits) == 3 or int(splits[0]) < 13):  # 如果是秒时分或月份
            IsLimitedLable = True
            return IsLimitedLable
        else:
            nowyear = datetime.datetime.now().year
            if((nowyear - int(splits[0]))<self.default_scope):#如果时限小于一年
                IsLimitedLable = True
                return IsLimitedLable
            else:#时限大于一年的话
                return IsLimitedLable










