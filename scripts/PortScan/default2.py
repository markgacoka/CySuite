# WORKS! Fastest so far...
# Runtime: 1.1055223941802979 second
import socket
from queue import Queue
from threading import Thread

import time
start_time = time.time()
SCAN_PORTS = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]# top 20

def scanhost(remoteServer):
    remoteServerIP  = socket.gethostbyname(remoteServer)
    try:
        output = []
        for port in SCAN_PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.settimeout(0.05)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                output.append(port)
            else:
                pass
            sock.close()
    except socket.gaierror:
        pass
    except socket.error:
        pass
    finally:
        return output

def scanner(ip, q):
    ports = scanhost(ip)
    if len(ports):
        q.put(ports)

def get_ports(target):
    q = Queue()    
    ip = socket.gethostbyname(target)

    try:
        t = Thread(target=scanner, args=[ip, q])
        t.start()
        return q.get()
    except:
        return []

target = 'markgacoka.com'
print(get_ports(target))
print("--- %s seconds ---" % (time.time() - start_time))