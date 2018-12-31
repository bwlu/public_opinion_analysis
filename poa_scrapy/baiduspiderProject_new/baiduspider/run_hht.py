import os
import threading
import time
import sys

def hhtscspider():
    os.system("scrapy crawl hhtcs")
    time.sleep(20)
def hhtgzspider():
    os.system("scrapy crawl hhtgz")
    time.sleep(20)
def hhtjl():
    os.system("scrapy crawl hhtjl")
    time.sleep(20)
def hhtxq():
    os.system("scrapy crawl hhtxq")
    time.sleep(20)
	
	
def run2():
    while(True):
        t2 = threading.Thread(target=hhtscspider)
    
        t2.start()
        t2.join()
        print("-------------------------------------------11111111111111111---------------------------------------------hhtsc 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run3():
    while(True):
        t3 = threading.Thread(target=hhtgzspider)
    
        t3.start()
        t3.join()
        print("------------------------------------------222222222222222222222------------------------------------------hhtgz 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run4():
    while(True):
        t4 = threading.Thread(target=hhtjl)
    
        t4.start()
        t4.join()
        print("------------------------------------------3333333333333333333------------------------------------------- hhtjl 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run5():
    while(True):
        t5 = threading.Thread(target=hhtxq)
    
        t5.start()
        t5.join()
        print("-----------------------------------------444444444444444444444444----------------------------------------hhtxq 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
		
def main():
    count = 0
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp
	
    threads = []

    tb = threading.Thread(target=run2)
    threads.append(tb)
    tc = threading.Thread(target=run3)
    threads.append(tc)
    td = threading.Thread(target=run4)
    threads.append(td) 
    te = threading.Thread(target=run5)
    threads.append(te)
	
    for t in threads:
        t.start()
    for t in threads:
        t.join()
		
    fp.close()
    sys.stderr = stderr
	
main()
		
