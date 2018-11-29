# -*- coding: utf-8 -*- 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
# import functools
from pyspark.streaming.kafka import KafkaUtils
from .pos_data import *

class CreateSC:
	sc = None
	def create_sc():
		if CreateSC.sc == None:
			CreateSC.sc = SparkContext("local[2]", "analysis")
			CreateSC.sc.setLogLevel("WARN")

try:
	CreateSC.create_sc()
	sc = CreateSC.sc
	# 设置时间为10秒
	ssc = StreamingContext(sc, 10)
	# 数据源
	# lines = ssc.textFileStream("/root/spark/share/")
	# sentences = lines.flatMap(lambda line:line.split('\n'))
	
	# zookeeper = '172.21.0.17:2181'
	# group_id = 'test-consumer-group'
	# topic = {'test':0}
	# sentences = KafkaUtils.createStream(ssc, zookeeper,group_id,topic)

	brokers ="127.0.0.1:9092"  
	topic='test'
	sentences = KafkaUtils.createDirectStream(ssc,[topic],kafkaParams={"metadata.broker.list":brokers})

	pairs = sentences.map(lambda sentence:ayls_sentence(sentence))
	# pairs.map(lambda x: (x[0], x[1])).pprint()
	pairs.pprint()
	filters = pairs.filter(lambda sentence:filter_sentence(sentence))
	filters.pprint()

	filters.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

	ssc.start()
	ssc.awaitTermination()

except Exception as e:
	print('&error&'*30)
	print(e)
	print('&error&'*30)


