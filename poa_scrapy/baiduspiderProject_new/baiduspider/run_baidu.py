import os
import threading
import time
import sys

def sbaiduspider():
    os.system("scrapy crawl sbaidu")

		
def main():
    count = 0
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp

    while True:
       ta = threading.Thread(target=sbaiduspider)
	
       ta.start()
       ta.join()
       print("-------------------------------------------------------------------sbaidu 执行完成一轮-------------")
       time.sleep(5)

    fp.close()
    sys.stderr = stderr
		
	
main()
