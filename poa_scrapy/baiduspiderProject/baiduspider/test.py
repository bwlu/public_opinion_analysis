import json
with open("UrlList.json","r",) as f:
    load = json.load(f)
print(type(load))
str = "https://tieba.baidu.com/p/3889492363"
print(str.split('/')[4])
#https://tieba.baidu.com/p/3889492363", "https://tieba.baidu.com/p/5506893515", "https://tieba.baidu.com/p/5936370728