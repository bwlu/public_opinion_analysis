#!/bin/bash
#根据进程名杀死进程
# 从命令行读取进程名称
NAME=$1 
echo "---------------"

echo $NAME '-> 正在停止'

# 过滤进程列表，不显示grep对应的进程，awk从第二列获取进程ID
ID=`ps -ef | grep "$NAME" | grep -v "grep" | grep -v 'stop_proc.sh' | awk '{print $2}'`
if [$ID -eq ''];then
echo '没有相关进程'
else
echo $NAME'相关进程:' $ID
fi
for id in $ID
    do
    # 杀掉进程`
    #ps aux|grep $id |grep -v grep
    #if [ $? -eq 0 ]
    #then
    #echo 'exist'
    kill -9 $id
    echo "killed the $NAME process $id"
    done

echo $NAME '-> 已停止'

echo "---------------"

