#!/bin/bash
echo '启动spark streaming'
ss='analysis.py'
cd poa_ss
function start_ss(){
	/usr/hdp/current/spark2-client/bin/spark-submit \
    --master spark://172.16.54.140:7078 \
    --jars spark-streaming-kafka-0-8-assembly_2.11-2.1.1.jar \
    --conf spark.yarn.maxAppAttempts=4 \
    --conf spark.yarn.am.attemptFailuresValidityInterval=1h \
    analysis.py
}
ps -fe|grep $ss |grep -v grep
if [ $? -ne 0 ]
then
start_ss
else
echo "spark streaming正在运行中......"
fi

