import json
def write_file(name,list):
    f = open('./jsonfile/'+name+'_UrlList.json', "w", encoding='UTF-8')
    content = json.dumps(list, ensure_ascii=False)
    f.write(content)
    f.close()
def read_file(name):
    try:
	    f = open('./jsonfile/'+name+'_UrlList.json', "r", encoding='UTF-8')  # 读取josn中的上次的链接
	    return json.load(f)  # 将数据存入列表
    except:
    	write_file(name,[])

