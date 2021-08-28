# Very fast
# Runtime: 0.5115261077880859 seconds
import socket
from queue import Queue
import threading

import time
start_time = time.time()

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((target, port))
        return True
    except:
        return False

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            open_ports.append(port)
        else:
            pass

def run_scanner(threads):
    ports = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
    for port in ports:
        queue.put(port)
    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    return open_ports

queue = Queue()
open_ports = []
domain = 'markgacoka.com'
target = socket.gethostbyname(domain)

print(run_scanner(100))
print("--- %s seconds ---" % (time.time() - start_time))