import datetime

def time_March(dataT,default_scope_day):
    IsLimitedLable = False  # 判断是否超过默认年限
    if(dataT.count('-')<1): # 如果是秒时分或几天内
        return True
    else:
        splits = dataT.split("-")
        if(dataT.count('-')==2):
            time = datetime.datetime(int(splits[0]), int(splits[1]), int(splits[2].split(' ')[0]))
        if(dataT.count('-')==1):
            time = datetime.datetime(int(splits[0]), int(splits[1]),15)
        deltatime = (datetime.datetime.now() - time).days
        if(deltatime<default_scope_day):#如果时限小于一年
            IsLimitedLable = True
            return IsLimitedLable
        else:#时限大于一年的话
            return IsLimitedLable
