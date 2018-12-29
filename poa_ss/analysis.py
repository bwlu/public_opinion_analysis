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
	sc.setLogLevel("WARN")
	# 设置时间为10秒
	ssc = StreamingContext(sc, 10)
	# 数据源

	brokers ="192.168.163.184:6667"  
	topic='postsarticles'
	sentences = KafkaUtils.createDirectStream(ssc,[topic],kafkaParams={"metadata.broker.list":brokers})
	
	pairs = sentences.map(lambda sentence:ayls_sentence(sentence))
	filters = pairs.filter(lambda sentence:filter_sentence(sentence))
	filters.pprint()

	filters.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

	ssc.start()
	ssc.awaitTermination()

except Exception as e:
	print('**error**'*10)
	print(e)
	print('**error**'*10)


