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
def wszgspider():
    os.system("scrapy crawl wszgcs")
    time.sleep(10)
    os.system("scrapy crawl wszgds")
    time.sleep(10)
    os.system("scrapy crawl wszgjd")
    time.sleep(10)
    os.system("scrapy crawl wszgzh")
def run():
    threads = []
    t1 = threading.Thread(target=sbaiduspider)
    threads.append(t1)
    t2 = threading.Thread(target=hhtspider)
    threads.append(t2)
    t3 = threading.Thread(target=jdwxspider)
    threads.append(t3)
    t4 = threading.Thread(target=wszgspider)
    threads.append(t4)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    time.sleep(100)#执行一轮后休眠时间

def main():
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp
    while(True):
        run()
    fp.close()
    sys.stderr = stderr
main()