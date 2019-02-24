# -*- coding: utf-8 -*- 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
from pyspark.streaming.kafka import KafkaUtils
# from pos_data import *
from oraclepool import (basd_info_add,sendPartition,ayls_sentence,filter_sentence)
import py4j
import time
import os

try:
	restart = True
	# sc = SparkContext("local[*]", "analysis")
	sc = SparkContext(appName="analysis")
	# sc.setLogLevel("DEBUG")
	sc.setLogLevel("WARN")
	# 设置时间为10秒
	ssc = StreamingContext(sc, 10)
	# 数据源

	brokers ="172.16.54.139:6667"
	topic='postsarticles'
	sentences = KafkaUtils.createDirectStream(ssc,[topic],kafkaParams={"metadata.broker.list":brokers})
	
	pairs = sentences.map(lambda sentence:ayls_sentence(sentence))
	filters = pairs.filter(lambda sentence:filter_sentence(sentence))
	filters.pprint()

	filters.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

	ssc.start()
	ssc.awaitTermination()

except py4j.protocol.Py4JJavaError as e:
	print('数据源错误，请检查kafka服务器是否运行正常，然后重启，已自动重启，若启动失败，请手动重启')
	log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	with open('../ERROR.log','w') as fp:
		fp.write('%s\n'%(log_time))
		fp.write('数据源错误，请检查kafka服务器是否运行正常，然后重启，已自动重启，若启动失败，请手动重启')
	if restart:
		restart = False
		print('10s后重启')
		time.sleep(10)
		os.system("./restart.sh")

except Exception as e:
	print('**error**'*10)
	print(e)
	print('**error**'*10)
	if restart:
		restart = False
		print('20s后重启')
		time.sleep(20)
		os.system("./restart.sh")


