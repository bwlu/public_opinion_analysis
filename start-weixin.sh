#!/bin/bash
echo '启动微信爬虫'
scrapy='sougouweixin.py'
ps -fe|grep $scrapy |grep -v grep
if [ $? -ne 0 ]
then
cd poa_scrapy
python3 sougouweixin.py
else
echo "微信爬虫正在运行中......"
fi

