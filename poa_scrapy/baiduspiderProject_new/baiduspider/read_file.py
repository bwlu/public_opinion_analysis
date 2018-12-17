import json
def read_file(name):
    f = open('./jsonfile/'+name+'_UrlList.json', "r", encoding='UTF-8')  # 读取josn中的上次的链接
    return json.load(f)  # 将数据存入列表
