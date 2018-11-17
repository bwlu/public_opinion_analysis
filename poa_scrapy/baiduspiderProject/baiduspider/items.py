# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    info = scrapy.Field()
    time = scrapy.Field()
    UrlId = scrapy.Field()
    childPage = scrapy.Field()
    #读取帖子内容的属性
