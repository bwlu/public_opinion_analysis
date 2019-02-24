#!/bin/bash
source /etc/profile
cd /home/public_sentiment
source ./stop_proc.sh weixin.py
sleep 2s
source ./stop_proc.sh sougouweixinhao.py
sleep 3s
echo '正在重新启动'
nohup ./start-weixin.sh > weixin_output.log 2>&1 &
sleep 5s
echo '删除文件'
rm -rf weixin_output.log
