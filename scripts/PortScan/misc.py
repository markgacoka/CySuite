# Very fast
# Runtime: 0.5115261077880859 seconds
import socket
from queue import Queue
import threading

# import time
# start_time = time.time()

class Portscanner:
    def __init__(self, domain):
        self.domain = domain
        self.target = socket.gethostbyname(domain)
        self.queue = Queue()
        self.open_ports = []

    def portscan(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((self.target, port))
            return True
        except:
            return False

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            if self.portscan(port):
                self.open_ports.append(int(port))
            else:
                pass

    def run_scanner(self, threads):
        ports = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
        for port in range(1, 65535+1):
            self.queue.put(port)
        thread_list = []

        for t in range(threads):
            thread = threading.Thread(target=self.worker)
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        return self.open_ports

# print("--- %s seconds ---" % (time.time() - start_time))