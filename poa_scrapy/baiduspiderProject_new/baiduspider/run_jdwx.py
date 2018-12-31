import os
import threading
import time
import sys

def jdwxbzspider():
    os.system("scrapy crawl jdwxbz")
    time.sleep(30)
def jdwxggspider():
    os.system("scrapy crawl jdwxgg")
    time.sleep(30)
def jdwxgqspider():
    os.system("scrapy crawl jdwxgq")
    time.sleep(30)
def jdwxtsspider():
    os.system("scrapy crawl jdwxts")
    time.sleep(30)
	
def run6():
    while(True):
        t6 = threading.Thread(target=jdwxbzspider)
    
        t6.start()
        t6.join()
        print("---------------------------------------111111111111111111111111---------------------------jdwxbz 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
	
def run7():
    while(True):
        t7 = threading.Thread(target=jdwxggspider)
    
        t7.start()
        t7.join()
        print("--------------------------------------22222222222222222222222-----------------------------jdwxgg 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run8():
    while(True):
        t8 = threading.Thread(target=jdwxgqspider)
    
        t8.start()
        t8.join()
        print("--------------------------------------3333333333333333333333------------------------------jdwxgq 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run9():
    while(True):
        t9 = threading.Thread(target=jdwxtsspider)
    
        t9.start()
        t9.join()
        print("------------------------------------44444444444444444444----------------------------------jdwxts 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
		
def main():
    count = 0
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp
	
    threads = []
	
    tf = threading.Thread(target=run6)
    threads.append(tf)
    tg = threading.Thread(target=run7)
    threads.append(tg)
    th = threading.Thread(target=run8)
    threads.append(th) 
    ti = threading.Thread(target=run9)
    threads.append(ti)
	
    for t in threads:
        t.start()
    for t in threads:
        t.join()
		
    fp.close()
    sys.stderr = stderr
	
	
main()
	
	
