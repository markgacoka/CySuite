# Very fast
# Runtime: 0.5115261077880859 seconds
import socket
from queue import Queue
import threading
import ssl
from http.client import responses

# import time
# start_time = time.time()

class Portscanner:
    def __init__(self, domain):
        self.domain = domain
        self.queue = Queue()
        self.chunk_size = 1024
        self.open_ports = []
        self.response = []
        self.status_code = ''
        self.ip_address = ''
        self.CRLF = "\r\n\r\n"

    def receive_all(sock, chunk_size=1024):
        chunks = []
        while True:
            chunk = sock.recv(int(chunk_size))
            if chunk:
                chunks.append(chunk)
            else:
                break
        return ''.join(chunks)

    def portscan(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            # tcp
            self.ip_address = socket.gethostbyname(self.domain)
            sock.connect((self.ip_address, port))
            # http
            req = "GET / HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\n\r\n".format(self.domain)
            sock.send(req.encode())
            self.response = sock.recv(4096).decode("UTF-8", errors='ignore').split('\r\n')
            self.status_code = self.response[0].split(' ')[1] + ' ' + responses[int(self.response[0].split(' ')[1])]
            sock.close()
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
        for port in ports:
            self.queue.put(port)
        thread_list = []

        for t in range(threads):
            thread = threading.Thread(target=self.worker)
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        return [self.open_ports, self.ip_address, self.status_code, self.response]

# print("--- %s seconds ---" % (time.time() - start_time))