#!/bin/bash
echo '启动spark streaming'
ss='analysis.py'
cd poa_ss
function start_ss(){
  /usr/hdp/current/spark2-client/bin/spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.1.1.jar analysis.py
}
ps -fe|grep $ss |grep -v grep
if [ $? -ne 0 ]
then
start_ss
else
echo "spark streaming正在运行中......"
fi

