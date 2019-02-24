#!/bin/bash
#
echo '正在重新启动'
nohup ./start-spark-streaming.sh > spark_output.log 2>&1 &
sleep 5s
echo '删除文件'
rm -rf spark_output.log
