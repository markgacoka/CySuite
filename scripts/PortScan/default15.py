# Fast but inaccurate
import socket
import time
import threading

from queue import Queue
socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = 'google.com'
t_IP = socket.gethostbyname(target)

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    open_ports = None
    try:
        con = s.connect((t_IP, port))
        with print_lock:
            print(port)
            open_ports = port
        con.close()
    except:
        pass
    return open_ports

def threader():
   while True:
      worker = q.get()
      portscan(worker)
      q.task_done()
      
q = Queue()
startTime = time.time()
   
for x in range(100):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()
   
portrange = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
for worker in portrange:
   q.put(worker)

print('Time taken:', time.time() - startTime)