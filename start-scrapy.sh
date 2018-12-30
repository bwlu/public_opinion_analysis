#!/bin/bash
echo '启动爬虫'
scrapy='together.py'
ps -fe|grep $scrapy |grep -v grep
if [ $? -ne 0 ]
then
cd poa_scrapy/baiduspiderProject_new/baiduspider
python3 together.py
else
echo "爬虫正在运行中......"
fi

