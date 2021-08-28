# Finds open, closed and filtered but output is ugly

import socket
import time
import _thread

ports = 100
url = 'markgacoka.com'
mode = 1024
ipurl = socket.gethostbyname(url)
f = open(ipurl, "a")

def start_scan(start, end):
    try:
        for x in range(start, end):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            res = sock.connect_ex((ipurl,x))
            if res == 0:
                tmp="Port",x,"is open", socket.getservbyport(x)
                tmp1=str(tmp[0])+" "+str(tmp[1])+" "+str(tmp[2])+" "+str(tmp[3])
                print(tmp1)
                f.write(str(tmp)+"\n")
        f.close()
    except Exception as e:
        print (e)

for count in range(ports):
    time.sleep(0.3)
    _thread.start_new_thread(start_scan, (count, count+1))
    if count > mode:
        exit(0)