# -*- coding: utf-8 -*-
from oraclepool import OrclPool
import json
import time
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

__all__ = ['basd_info_add','sendPartition','ayls_sentence','filter_sentence']

def update_keywords():
	keywords = []
	op = OrclPool()
	sql = 'select * from BASE_ANALYSIS_SENTIMENT where DICT_ENABLED_VALUE=300010000000001'
	key_list = op.fetch_all(sql)
	for ld in key_list:
		key = {}
		key['id'] = ld[0]
		key['name'] = ld[1]
		key['main_word'] = ld[2]
		key['key_word'] = ld[2].split(',')
		keywords.append(key)
	return keywords

def basd_info_add(sql):
	try:
		op = OrclPool()
		op.execute_sql(sql)
		print('插入数据库')
		# print(sql)
	except Exception as e:
		if sql != 'insert all select 1 from dual':
			export_log({"type":"批量插入sql","data":sql,"exception":str(e)})

def sendPartition(iter):
	sql = 'insert all '
	b = False
	for record in iter:
		try:
			b = True
			res = json.loads(record[0])
			sqld = "into BASE_ANALYSIS_SENTIMENT_DETAIL(PID,NAME,MAIN_WORD,key_WORD,TITLE,INTRODUCTION,URL,OCCUR_TIME,ORIGIN_VALUE,ORIGIN_NAME) "
			sqld += "values("+str(record[1])+",'"+record[2]+"','"+record[3]+"','"+record[4]+"'"
			split_len = len(res['OCCUR_TIME'].split('-'))-1
			occur_time = res['OCCUR_TIME']
			if len(occur_time)<15:
				if split_len==1:
					occur_time = "%s-01 00:00:00"%occur_time
				elif split_len==2:
					occur_time = "%s 00:00:00"%occur_time
				else:
					occur_time = "%s-01-01 00:00:00"%occur_time
			else:
				occur_time = "%s"%res['OCCUR_TIME']
			try:
				time.strptime(occur_time,"%Y-%m-%d %H:%M:%S")
			except:
				export_log({"type":"时间处理错误","data":res})
				occur_time = "2000-01-01 00:00:00"
			if res['INTRODUCTION'] != '':
				res['TITLE'] = res['TITLE'].replace('\'','"')
				res['INTRODUCTION'] = res['INTRODUCTION'].replace('\'','"')
				sqld += ",'"+res['TITLE']+"','"+res['INTRODUCTION']+"','"+res['URL']+"',to_timestamp('"+occur_time+"','yyyy-mm--dd hh24:mi:ss.ff'),"+res['ORIGIN_VALUE']+",'"+res['ORIGIN_NAME']+"') "
				sql += sqld
			else:
				if res['ORIGIN_VALUE'] == '500010000000002':
					export_log({"type":"没有简介","data":res})
				else:
					export_log({"type":"没有阅读权限","data":res})
		except:
			export_log({"type":"拼接sql","data":record[0]})
	sql += "select 1 from dual"
	if b:
		basd_info_add(sql)
	
def ayls_sentence(sentence):
	keywords = update_keywords()
	
	for key in keywords:
		for kw in key['key_word']:
			if kw in sentence[1]:
				# print(kw)
				return (sentence[1],key['id'],key['name'],key['main_word'],kw)
	return (sentence,0)

def filter_sentence(sentence):
	if sentence[1] == 0:
		return False
	return True

def export_log(log_info):
	log_time = time.strftime("%Y-%m-%d", time.localtime())
	log_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if not os.path.exists('/tmp/log/log_poa/'):
		os.makedirs('/tmp/log/log_poa/')
	# fp =open('/tmp/log/log_poa/%s.log'%log_time,'a+')
	with open('/tmp/log/log_poa/streaming-%s.log'%log_time,'a+') as fp:
		fp.write('%s:%s'%(log_time1,json.dumps(log_info,ensure_ascii=False)))
		fp.write('\n')
	# fp.close()
	
