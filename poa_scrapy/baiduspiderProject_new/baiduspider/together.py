import os
import threading
import time
import sys
def sbaiduspider():
    os.system("scrapy crawl sbaidu")
def hhtspider():
    os.system("scrapy crawl hhtcs")
    time.sleep(10)
    os.system("scrapy crawl hhtgz")
    time.sleep(10)
    os.system("scrapy crawl hhtjl")
    time.sleep(10)
    os.system("scrapy crawl hhtxq")
def jdwxspider():
    os.system("scrapy crawl jdwxbz")
    time.sleep(10)
    os.system("scrapy crawl jdwxgg")
    time.sleep(10)
    os.system("scrapy crawl jdwxgq")
    time.sleep(10)
    os.system("scrapy crawl jdwxts")
def wszgcsspider():
    os.system("scrapy crawl wszgcs")
def wszgdsspider():
    os.system("scrapy crawl wszgds")
def wszgjdspider():
    os.system("scrapy crawl wszgjd")
def wszgzhspider():
    os.system("scrapy crawl wszgzh")
def run(count):
    threads = []
    t1 = threading.Thread(target=sbaiduspider)
    threads.append(t1)
    t2 = threading.Thread(target=hhtspider)
    threads.append(t2)
    t3 = threading.Thread(target=jdwxspider)
    threads.append(t3)
    if(count==5):
        t4 = threading.Thread(target=wszgcsspider)
        threads.append(t4)
        t5 = threading.Thread(target=wszgdsspider)
        threads.append(t5)
        t6 = threading.Thread(target=wszgjdspider)
        threads.append(t6)
        t7 = threading.Thread(target=wszgzhspider)
        threads.append(t7)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print("执行完成一轮")
    time.sleep(30)#执行一轮后休眠时间

def main():
    count = 5
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp
    while(True):
        run(count)
        if(count==5): count=0
        count=count+1
    fp.close()
    sys.stderr = stderr
main()