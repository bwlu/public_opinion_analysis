# -*- coding: utf-8 -*- 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
from pyspark.streaming.kafka import KafkaUtils
from pos_data import *

try:
	sc = SparkContext("local[*]", "analysis")
	# sc = SparkContext(appName="analysis")
	# sc.setLogLevel("DEBUG")
	# 设置时间为10秒
	ssc = StreamingContext(sc, 10)
	# 数据源
	
	# zookeeper = '192.168.163.184:2181'
	# group_id = 'test-consumer-group'
	# topic = {'test':0}
	# sentences = KafkaUtils.createStream(ssc, zookeeper,group_id,topic)

	brokers ="192.168.163.184:6667"  
	topic='test'
	sentences = KafkaUtils.createDirectStream(ssc,[topic],kafkaParams={"metadata.broker.list":brokers})
	sentences.pprint()
	# pairs = sentences.map(lambda sentence:ayls_sentence(sentence))
	# filters = pairs.filter(lambda sentence:filter_sentence(sentence))
	# filters.pprint()

	# filters.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

	ssc.start()
	ssc.awaitTermination()

except Exception as e:
	print('**error**'*10)
	print(e)
	print('**error**'*10)

