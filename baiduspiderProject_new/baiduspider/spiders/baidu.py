# -*- coding: utf-8 -*-
import scrapy
from baiduspider.items import BaiduspiderItem

#这个里面已经实现了访问帖子内部的方法
class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    content = '户户通'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw='+content]

    def parse(self, response):
        nodelist = response.xpath('//div[@class="col2_right j_threadlist_li_right "]')
        item = BaiduspiderItem()
        NextPageUrl = ''
        for node in nodelist:
            item["title"]= node.xpath("./div[1]/div/a[@title]/text()").extract_first()
            item["UrlId"] = node.xpath("./div[1]/div/a[@href]/@href").extract_first()
            item["info"] = node.xpath('./div[2]/div[@class="threadlist_text pull_left"]/div[1]/text()').extract_first()
            item["time"] = node.xpath('./div[1]/div[2]/span[@title="创建时间"]/text()').extract_first()

            childUrl = "https://tieba.baidu.com" + item["UrlId"]
            item["UrlId"] = childUrl
            if(NextPageUrl == ''):
                NextPageUrl = 'https:'+ response.xpath('//a[@class = "next pagination-item "]/@href').extract_first()
            #读取帖子详细信息的方法，但需求中不需要,实际只需使用使用'baidu2'即可，若用此方法需开启items中的childPage
            request = scrapy.Request(childUrl,callback =self.ChildPage)
            request.meta['item'] = item
            yield request

        yield scrapy.Request('https://tieba.baidu.com/f?kw=%E6%88%B7%E6%88%B7%E9%80%9A&ie=utf-8&pn=50',callback = self.parse)
        print("翻页了！！！！！！！！！！！！！！！！！")





    def ChildPage(self,response):

        temp = response.meta["item"]
        #print("____________infomation__________")
        #print(temp["title"])
        #print(temp["UrlId"])
        #print(temp["info"].strip())
        #print(temp["time"].strip())
        temp["info"] = temp["info"].strip()
        temp["time"] = temp["time"].strip()
        content_page = []
        childlist = response.xpath('//cc/div[@class="d_post_content j_d_post_content "]/text()').extract()
        #print("______________content___________________")
        for node in childlist:
            str_ = str(node)
            content_page.append(str_.strip())
            print(str_.strip() + "\n")
        #print("_______________OVER___________________")
        temp['childPage'] = content_page
        response.meta['item'] = temp
        yield response.meta['item']




