# Extremely fast
# Runtime:  0.18525075912475586 seconds
import socket
import time
start_time = time.time()

class Portscan:
    def __init__(self, target):
        self.target = target
        self.open_ports = []

    def scan_port(self, port):
        target = 'markgacoka.com'
        remoteHost = socket.gethostbyname(target)
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(0.05)
            result = sock.connect_ex((remoteHost,port))
            if result == 0:
                self.open_ports.append(port)
                sock.close()
        except:
            pass
        return self.open_ports

import multiprocessing as mp
import itertools

final_lst = []
domain = 'markgacoka.com'
portscan = Portscan(domain)
portrange = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
p = mp.Pool()
final_lst = list(itertools.chain.from_iterable(p.map(portscan.scan_port, portrange)))
print(final_lst)

print("--- %s seconds ---" % (time.time() - start_time))
