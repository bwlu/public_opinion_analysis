import os
import threading
import time
import sys

def wszgcsspider():
    os.system("scrapy crawl wszgcs")
    time.sleep(30)
def wszgdsspider():
    os.system("scrapy crawl wszgds")
    time.sleep(30)
def wszgjdspider():
    os.system("scrapy crawl wszgjd")
    time.sleep(30)
def wszgzhspider():
    os.system("scrapy crawl wszgzh")
    time.sleep(30)
	
def run10():
    while(True):
        t10 = threading.Thread(target=wszgcsspider)
    
        t10.start()
        t10.join()
        print("---------------------11111111111111111111----------------------wszgcs 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run11():
    while(True):
        t11 = threading.Thread(target=wszgdsspider)
    
        t11.start()
        t11.join()
        print("-----------------------2222222222222222222222222---------------wszgds 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run12():
    while(True):
        t12 = threading.Thread(target=wszgjdspider)
    
        t12.start()
        t12.join()
        print("---------------------333333333333333333------------------------wszgjd 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def run13():
    while(True):
        t13 = threading.Thread(target=wszgzhspider)
    
        t13.start()
        t13.join()
        print("--------------------------444444444444444444--------------------wszgzh 执行完成一轮")
        time.sleep(10)#执行一轮后休眠时间
		
def main():
    count = 0
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp
	
    threads = []

    tj = threading.Thread(target=run10)
    threads.append(tj)
    tk = threading.Thread(target=run11)
    threads.append(tk)
    tl = threading.Thread(target=run12)
    threads.append(tl)
    tm = threading.Thread(target=run13)
    threads.append(tm)

    for t in threads:
        t.start()
    for t in threads:
        t.join() 

    fp.close()
    sys.stderr = stderr
	
main()	
		
