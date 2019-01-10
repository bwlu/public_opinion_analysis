#!/bin/bash
echo '启动spark streaming'
ss='analysis.py'
cd poa_ss
function start_ss(){
	/usr/hdp/current/spark2-client/bin/spark-submit \
    --master yarn \
    --deploy-mode client  \
    --jars spark-streaming-kafka-0-8-assembly_2.11-2.1.1.jar \
    --executor-memory 4096m \
    --driver-memory 4096m  \
    --driver-cores 1 \
    --executor-cores 3 \
    --conf spark.default.parallelism=3 \
    --conf spark.ui.port=7077 \
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

