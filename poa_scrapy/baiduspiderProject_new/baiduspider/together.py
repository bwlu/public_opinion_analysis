import os
import threading
import time
import sys
def sbaiduspider():
    os.system("scrapy crawl sbaidu")
def hhtscspider():
    os.system("scrapy crawl hhtcs")
    time.sleep(10)
def hhtgzspider():
    os.system("scrapy crawl hhtgz")
    time.sleep(10)
def hhtjl():
    os.system("scrapy crawl hhtjl")
    time.sleep(10)
def hhtxq():
    os.system("scrapy crawl hhtxq")
	time.sleep(10)
def jdwxbzspider():
    os.system("scrapy crawl jdwxbz")
    time.sleep(10):
def jdwxggspider()
    os.system("scrapy crawl jdwxgg")
    time.sleep(10)
def jdwxgqspider():
    os.system("scrapy crawl jdwxgq")
    time.sleep(10)
def jdwxtsspider():
    os.system("scrapy crawl jdwxts")
	time.sleep(10)
def wszgcsspider():
    os.system("scrapy crawl wszgcs")
    time.sleep(10)
def wszgdsspider():
    os.system("scrapy crawl wszgds")
    time.sleep(10)
def wszgjdspider():
    os.system("scrapy crawl wszgjd")
    time.sleep(10)
def wszgzhspider():
    os.system("scrapy crawl wszgzh")
	time.sleep(10)
	
	
def run1():
    while(True):
        t1 = threading.Thread(target=sbaiduspider)
    
        t.start()
        t.join()
        print(" Sbaidu  执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run2():
    while(True):
        t1 = threading.Thread(target=hhtscspider)
    
        t.start()
        t.join()
        print(" hhtsc 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run3():
    while(True):
        t1 = threading.Thread(target=hhtgzspider)
    
        t.start()
        t.join()
        print(" hhtgz 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run4():
    while(True):
        t1 = threading.Thread(target=hhtjl)
    
        t.start()
        t.join()
        print(" hhtjl 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run5():
    while(True):
        t1 = threading.Thread(target=hhtxq)
    
        t.start()
        t.join()
        print(" hhtxq 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run6():
    while(True):
        t1 = threading.Thread(target=jdwxbzspider)
    
        t.start()
        t.join()
        print(" jdwxbz 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
	
def run7():
    while(True):
        t1 = threading.Thread(target=jdwxggspider)
    
        t.start()
        t.join()
        print(" jdwxgg 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run8():
    while(True):
        t1 = threading.Thread(target=jdwxgqspider)
    
        t.start()
        t.join()
        print(" jdwxgq 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run9():
    while(True):
        t1 = threading.Thread(target=jdwxtsspider)
    
        t.start()
        t.join()
        print(" jdwxts 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run10():
    while(True):
        t1 = threading.Thread(target=wszgcsspider)
    
        t.start()
        t.join()
        print(" wszgcs 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run11():
    while(True):
        t1 = threading.Thread(target=wszgdsspider)
    
        t.start()
        t.join()
        print(" wszgds 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run12():
    while(True):
        t1 = threading.Thread(target=wszgjdspider)
    
        t.start()
        t.join()
        print(" wszgjd 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		
def run13():
    while(True):
        t1 = threading.Thread(target=wszgzhspider)
    
        t.start()
        t.join()
        print(" wszgzh 执行完成一轮")
	    time.sleep(100)#执行一轮后休眠时间
		

	
def main():
    count = 0
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp
	
	threads = []

    ta = threading.Thread(target=run1)
    threads.append(ta)
    tb = threading.Thread(target=run2)
    threads.append(tb)
	tc = threading.Thread(target=run3)
    threads.append(tc)
    td = threading.Thread(target=run4)
    threads.append(td)
	te = threading.Thread(target=run5)
    threads.append(te)
    tf = threading.Thread(target=run6)
    threads.append(tf)
	tg = threading.Thread(target=run7)
    threads.append(tg)
    th = threading.Thread(target=run8)
    threads.append(th)
	ti = threading.Thread(target=run9)
    threads.append(ti)
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