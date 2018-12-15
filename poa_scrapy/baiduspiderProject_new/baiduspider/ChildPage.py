import requests
from lxml import etree
def ChildPage(childUrl,spider):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    response = requests.get(childUrl, headers=headers)
    root = etree.HTML(response.content)
    if spider== '2' or spider=='1':
        text = root.xpath("//td[@class='t_f']/text()")  # 第一个节点
        strs = text[0]
        s = str(strs)  # 简介内容
        if (len(s) == 2):  # 如果为空字符串，再处理,还有点问题
            list_text = root.xpath("//td[@class='t_f']//text()")
            isstart = False
            content = ''
            if(spider=='1'): #1为hht 2为jdwx 3为wszg
                for t in list_text:
                    if ("发表于" in t):
                        break
                    if (isstart):
                        content = content + str(t) + ' '
                    if ('编辑' in t):
                        isstart = True
            if (spider == '2'):  # 1为hht 2为jdwx 3为wszg
                for t in list_text:
                    if ("发表于" in t):
                        break
                    if (isstart):
                        content = content + str(t) + ' '
                    if ('x' in t):
                        isstart = True
            s = str(content)
    if spider =='3':
        content=''
        list_text = root.xpath("//td[@class='t_f']//text()")
        for t in list_text:
            content = content + str(t) + ' '
        s = content[:800]
    info = ",".join(s.split())
    return info