# Very very fast and works!
# Runtime: 1.0313730239868164 seconds
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

class PortScan:
    def __init__(self, target):
        self.open_ports = []
        self.target = target

    def portscan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.05)
        try:
            con = s.connect((target,port))
            self.open_ports.append(port)
            con.close()
        except: 
            pass
        else:
            return self.open_ports
        
portrange = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
target = 'markgacoka.com'

portscan_inst = PortScan(target)
for port in portrange:
    t = ThreadWithReturnValue(target=portscan_inst.portscan, args=(port, )) 
    t.start()
    t.join()
print(portscan_inst.open_ports)
print("--- %s seconds ---" % (time.time() - start_time))