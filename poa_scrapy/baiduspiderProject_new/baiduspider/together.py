import os
import threading
import time
import sys
def sbaiduspider():
    os.system("scrapy crawl sbaidu")
    time.sleep(100)
def hhtscspider():
    os.system("scrapy crawl hhtcs")
    time.sleep(50)
def hhtgzspider():
    os.system("scrapy crawl hhtgz")
    time.sleep(50)
def hhtjl():
    os.system("scrapy crawl hhtjl")
    time.sleep(50)
def hhtxq():
    os.system("scrapy crawl hhtxq")
    time.sleep(50)
def jdwxbzspider():
    os.system("scrapy crawl jdwxbz")
    time.sleep(50)
def jdwxggspider():
    os.system("scrapy crawl jdwxgg")
    time.sleep(50)
def jdwxgqspider():
    os.system("scrapy crawl jdwxgq")
    time.sleep(50)
def jdwxtsspider():
    os.system("scrapy crawl jdwxts")
    time.sleep(50)
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
    
        t1.start()
        t1.join()
        print(" Sbaidu  执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run2():
    while(True):
        t2 = threading.Thread(target=hhtscspider)
    
        t2.start()
        t2.join()
        print(" hhtsc 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run3():
    while(True):
        t3 = threading.Thread(target=hhtgzspider)
    
        t3.start()
        t3.join()
        print(" hhtgz 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run4():
    while(True):
        t4 = threading.Thread(target=hhtjl)
    
        t4.start()
        t4.join()
        print(" hhtjl 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run5():
    while(True):
        t5 = threading.Thread(target=hhtxq)
    
        t5.start()
        t5.join()
        print(" hhtxq 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		 
def run6():
    while(True):
        t6 = threading.Thread(target=jdwxbzspider)
    
        t6.start()
        t6.join()
        print(" jdwxbz 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
	
def run7():
    while(True):
        t7 = threading.Thread(target=jdwxggspider)
    
        t7.start()
        t7.join()
        print(" jdwxgg 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run8():
    while(True):
        t8 = threading.Thread(target=jdwxgqspider)
    
        t8.start()
        t8.join()
        print(" jdwxgq 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run9():
    while(True):
        t9 = threading.Thread(target=jdwxtsspider)
    
        t9.start()
        t9.join()
        print(" jdwxts 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run10():
    while(True):
        t10 = threading.Thread(target=wszgcsspider)
    
        t10.start()
        t10.join()
        print(" wszgcs 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run11():
    while(True):
        t11 = threading.Thread(target=wszgdsspider)
    
        t11.start()
        t11.join()
        print(" wszgds 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run12():
    while(True):
        t12 = threading.Thread(target=wszgjdspider)
    
        t12.start()
        t12.join()
        print(" wszgjd 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		
def run13():
    while(True):
        t13 = threading.Thread(target=wszgzhspider)
    
        t13.start()
        t13.join()
        print(" wszgzh 执行完成一轮")
        time.sleep(20)#执行一轮后休眠时间
		

	
def main():
    print(11)
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
    print(22)  

    fp.close()
    sys.stderr = stderr
main()
