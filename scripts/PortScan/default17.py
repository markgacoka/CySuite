# Very very fast and works!
from threading import Thread
import socket
import time
start_time = time.time()

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)# 
    open_port = None
    try:
        con = s.connect((target,port))
        open_port = port
        print(open_port)
        con.close()
    except: 
        pass
    else:
        return open_port

def get_ports(target, portrange):
    for port in portrange: 
        t = ThreadWithReturnValue(target=portscan, args=(port, )) 
        t.start()
        if t.join() != None:
            print(t.join())

portrange = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
target = 'markgacoka.com'
print(get_ports(target, portrange))
print("--- %s seconds ---" % (time.time() - start_time))