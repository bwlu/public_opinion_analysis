#!/bin/bash
source /etc/profile
cd /home/public_sentiment
source ./stop_proc.sh together.py
sleep 2s
source ./stop_proc.sh scrapy
sleep 3s
echo '正在重新启动'
nohup ./start-scrapy.sh > scrapy_output.log 2>&1 &
sleep 5s
echo '删除文件'
rm -rf scrapy_output.log
