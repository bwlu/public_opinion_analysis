#!/bin/bash
source /etc/profile
cd /home/public_sentiment
source ./stop_proc.sh streaming
sleep 2s
source ./stop_proc.sh analysis.py
sleep 3s
echo '正在重新启动'
nohup ./start-spark-streaming.sh > spark_output.log 2>&1 &
sleep 5s
echo '删除文件'
rm -rf spark_output.log
