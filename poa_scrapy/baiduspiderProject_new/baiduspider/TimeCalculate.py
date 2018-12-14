import time
import datetime
def time_calculate(time,origin):

    if origin=='sbaidu':
       if time.find(':')!=-1:
           time = str(datetime.datetime.now().strftime('%Y-%m-%d'))+" "+time
           return time+':00'
       else:
           if(int(time.split('-')[0])>1000):
               return time
           else:
               time = str(datetime.datetime.now().year)+"-"+time
               return time

    else:
        if time.count('-')==2:
            return time
        if time.find('刚'):
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 得到今天日期
            return str(time)
        if time.find('天前')==2:
            day = time[0:1]
            delta = datetime.timedelta(days=int(day))
            time = datetime.datetime.now().strftime('%Y-%m-%d')#得到今天日期
            time = datetime.datetime.strptime(time, '%Y-%m-%d')#转换成时间格式
            time = time - delta
            return str(time)
        if time.find('小时')==2:
            hour = time[0:1]
            if(hour=='半'):
                delta = datetime.timedelta(minutes=30)
            else:
                delta = datetime.timedelta(hours=int(hour))
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 得到今天日期
            time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')  # 转换成时间格式
            time = time - delta
            return str(time)
        if time.find('分钟')==2:
            minute = time[0:1]
            delta = datetime.timedelta(minutes=int(minute))
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 得到今天日期
            time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')  # 转换成时间格式
            time = time - delta
            return str(time)
        if time.find('昨天')==0:
            delta = datetime.timedelta(days=1)
            date = datetime.datetime.now().strftime('%Y-%m-%d')# 得到今天日期
            date = datetime.datetime.strptime(date, '%Y-%m-%d')  # 转换成时间格式
            date = date - delta#减一天
            time = date.strftime('%Y-%m-%d')+' '+ time[3:]+":00"
            return str(time)
        if time.find('前天')==0:
            delta = datetime.timedelta(days=2)
            date = datetime.datetime.now().strftime('%Y-%m-%d')# 得到今天日期
            date = datetime.datetime.strptime(date, '%Y-%m-%d')  # 转换成时间格式
            date = date - delta#减一天
            print(time[3:])
            time = date.strftime('%Y-%m-%d')+' '+ time[3:]+":00"
            return str(time)




