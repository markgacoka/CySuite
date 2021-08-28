# WORKS! Fastest so far...
import socket

from queue import Queue
from threading import Thread

def scanhost(remoteServer):
    remoteServerIP  = socket.gethostbyname(remoteServer)
    try:
        output = []
        for port in SCAN_PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.settimeout(0.2)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                output.append(port)
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

q = Queue()
SCAN_PORTS = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]# top 20

target = 'markgacoka.com'
ip = socket.gethostbyname(target)

try:
    t = Thread(target=scanner, args=[ip, q])
    t.start()
    print(q.get())
except:
    raise