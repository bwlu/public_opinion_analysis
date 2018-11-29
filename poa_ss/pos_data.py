from orcl_pool import OrclPool
import json
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

__all__ = ['update_keywords','basd_info_add','sendPartition','ayls_sentence','filter_sentence']

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
	# op = OrclPool()
	# op.execute_sql(sql)
	print(sql)

def sendPartition(iter):
	sql = 'insert all '
	b = False
	for record in iter:
		b = True
		print(type(record[0]))
		print(record[0])
		print(record)
		res = json.loads(record[0])
		sqld = "into BASE_ANALYSIS_SENTIMENT_DETAIL(PID,NAME,MAIN_WORD,key_WORD,TITLE,INTRODUCTION,URL,OCCUR_TIME,ORIGIN_VALUE,ORIGIN_NAME) "
		sqld += "values("+str(record[1])+",'"+record[2]+"','"+record[3]+"','"+record[4]+"'"
		sqld += ",'"+res['TITLE']+"','"+res['INTRODUCTION']+"','"+res['URL']+"',to_timestamp('"+res['OCCUR_TIME']+"','yyyy-mm--dd hh24:mi:ss.ff'),"+res['ORIGIN_VALUE']+",'"+res['ORIGIN_NAME']+"') "
		sql += sqld
	sql += "select 1 from dual"
	if b:
		basd_info_add(sql)
	
def ayls_sentence(sentence):
	keywords = update_keywords()
	# keywords = [{'id':1,'name':'户户通','main_word':'户户通,恶意,安装','key_word':['户户通','恶意','安装']}]
	for key in keywords:
		for kw in key['key_word']:
			if kw in sentence[1]:
				print(kw)
				return (sentence[1],key['id'],key['name'],key['main_word'],kw)
	return (sentence,0)

def filter_sentence(sentence):
	if sentence[1] == 0:
		return False
	return True
