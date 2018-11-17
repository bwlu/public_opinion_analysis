# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from kafka import KafkaProducer   #引入包，如果你在自己的电脑上跑，得先安装kafka
import time

class BaiduspiderPipeline(object):
    def process_item(self, item, spider):
        # 创建一个生产者，连接到指定的消息队列上
        producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])

        # 数据类型，假设这个为单条数据
        dict1 = list(item)
        while True:
            msg = str(dict1)  # 将数据转成字符串
            print(msg)
            # 发送topic为information的数据（information相当于表名，每条数据记录相当于表中的一行）
            producer.send('information', msg.encode('utf-8'))
            time.sleep(1)
        # 停止生产数据
        producer.close()

        return item
