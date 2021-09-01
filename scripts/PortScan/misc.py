# Very fast
# Runtime: 0.5115261077880859 seconds
from queue import Queue
import threading
import pycurl
import socket
from http.client import responses
from io import BytesIO

# import time
# start_time = time.time()

class Portscanner:
    def __init__(self, domain):
        self.domain = domain
        self.queue = Queue()
        self.open_ports = []
        self.response = []
        self.status_code = None
        self.ip_address = None
        self.CRLF = "\r\n\r\n"

    def portscan(self, port):
        open_port = False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            # tcp
            self.ip_address = socket.gethostbyname(self.domain)
            is_open = sock.connect((self.ip_address, port))
            # http
            c = pycurl.Curl()
            e = BytesIO()
            c.setopt(pycurl.URL, 'http://' + self.domain)
            c.setopt(pycurl.HTTPHEADER, [
                'Accept: */*',
                'Content-Type: application/octet-stream',
                'User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
                'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language: en-us,en;q=0.5',
                'Accept-Encoding: gzip,deflate',
                'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive: 300',
                'Connection: keep-alive',
                ])
            c.setopt(pycurl.NOBODY, True)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.TIMEOUT_MS, 3000)
            c.setopt(pycurl.WRITEFUNCTION, e.write)
            c.perform()
            self.status_code = str(c.getinfo(pycurl.RESPONSE_CODE)) + ' ' + responses[int(c.getinfo(pycurl.RESPONSE_CODE))]
            self.response = e.getvalue().decode('UTF-8')
            c.close()
            sock.close()
            if is_open == None:
                open_port = True
        except:
            return open_port
        finally:
            return open_port

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            if self.portscan(port):
                self.open_ports.append(int(port))
            else:
                pass

    def run_scanner(self, threads):
        # most common ports
        ports = [1, 5, 7, 18, 20, 21, 22, 23, 25, 37, 42, 43, 49, 53, 67, 
        68, 69, 70, 79, 80, 81, 82, 88, 101, 109, 110, 115, 119, 123, 137, 
        138, 139, 143, 156, 161, 162, 179, 183, 194, 389, 443, 444, 445, 546, 547,
        554, 563, 587, 636, 993, 995, 1023, 1080, 1723, 2077, 2078, 2082, 
        2083, 2086, 2087, 2095, 2096, 3306, 3389, 5900, 8080, 31337, 33434, 33848]

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
        return [self.open_ports, self.ip_address, self.status_code, self.response[20:]]

subdomains = ["markgacoka.com","webmail.markgacoka.com","fun.markgacoka.com","cpanel.markgacoka.com","webdisk.fun.markgacoka.com","mail.markgacoka.com","dc-9ab17c78bc2d.markgacoka.com","webdisk.markgacoka.com","blog.markgacoka.com","cpanel.fun.markgacoka.com","www.fun.markgacoka.com","www.markgacoka.com","webmail.fun.markgacoka.com"]
for subdomain in subdomains:
    portscanner = Portscanner(subdomain)
    port, ip, status, response_header = portscanner.run_scanner(100)
    print(port, ip, status, response_header)
# # print("--- %s seconds ---" % (time.time() - start_time))