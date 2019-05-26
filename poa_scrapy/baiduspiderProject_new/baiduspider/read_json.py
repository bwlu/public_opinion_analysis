import json
def read_json(name):
    try:
        if(name == 'sbaidu'):
            f = open("./jsonfile/baidu_UrlList.json", "r", encoding='UTF-8')
        else:
            f = open("./jsonfile/"+name+'_UrlList.json', "r", encoding='UTF-8')  # 读取josn中的上次的链接
        return False
    except:
        print("首次爬取")
        return True