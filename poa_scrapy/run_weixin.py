import os
import threading
import time
import sys

def weixinspider():
    os.system("python3 sougouweixinhao.py")

		
def main():
    count = 0
    fp = open('out_put', 'w')#用来输出错误信息
    stderr = sys.stderr
    sys.stderr = fp

    while True:
       t = threading.Thread(target=weixinspider)
	
       t.start()
       t.join()
       print(" weixin 执行完成一轮")
       time.sleep(10)

    fp.close()
    sys.stderr = stderr
		
	
main()
