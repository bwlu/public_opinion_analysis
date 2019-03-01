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
	sc = SparkContext("local[*]", "analysis")
	# sc = SparkContext(appName="analysis")
	# sc.setLogLevel("DEBUG")
	sc.setLogLevel("WARN")
	# 设置时间为10秒
	ssc = StreamingContext(sc, 10)
	# 数据源
	# brokers ="172.16.54.139:6667"
	brokers ="172.16.54.148:6667,172.16.54.139:6667,172.16.54.140:6667,172.16.54.141:6667"
	topic='postsarticles'
	sentences = KafkaUtils.createDirectStream(ssc,[topic],kafkaParams={"metadata.broker.list":brokers})
	
	pairs = sentences.map(lambda sentence:ayls_sentence(sentence))
	filters = pairs.filter(lambda sentence:filter_sentence(sentence))
	filters.pprint()

	filters.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

	ssc.start()
	ssc.awaitTermination()

except py4j.protocol.Py4JJavaError as e:
	fn = 'DATA_SOURCE_ERROR'
	print('数据源错误，请检查kafka服务器是否运行正常，然后重启，已自动重启，若启动失败，请手动重启')
	restart = False
	log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if os.path.exists('../%s.log'%fn):
		mtime = os.path.getmtime('../%s.log'%fn) #获取创建时间
		m_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
		if log_time.split(':')[0]==m_time.split(':')[0]: #如果当天一小时内重启过，则生成错误日志
			restart = False
		else:
			restart = True
	else:
		restart = True
	with open('../%s.log'%fn,'w') as fp:
		fp.write('%s\n'%(log_time))
		fp.write('数据源错误，请检查kafka服务器是否运行正常，然后重启，已自动重启，若启动失败，请手动重启\n')
		fp.write('%s\n'%str(e))
	print('已生成日志：%s.log\n'%fn)
	if restart:
		print('30s后重启')
		time.sleep(30)
		os.system("./restart.sh")

except Exception as e:
	fn = 'ELSE_ERROR'
	print('**error**'*10)
	restart = False
	log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if os.path.exists('../%s.log'%fn):
		mtime = os.path.getmtime('../%s.log'%fn) #获取创建时间
		m_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
		if log_time.split(':')[0]==m_time.split(':')[0]: #如果当天一小时内重启过，则生成错误日志
			restart = False
		else:
			restart = True
	else:
		restart = True
	print(e)
	with open('../%s.log'%fn,'w') as fp:
		fp.write('%s\n'%(log_time))
		fp.write('%s\n'%str(e))

	print('**error**'*10)
	print('已生成日志：%s.log\n'%fn)
	if restart:
		print('30s后重启')
		time.sleep(30)
		os.system("./restart.sh")
