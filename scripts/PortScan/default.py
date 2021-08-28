# Displays all open ports, scans until 1024
# Works occasionaly
import socket
import threading
import time
start_time = time.time()

def banner(host ,port):
    data = s.connect((host ,port))
    return data.recv(1024)

def scanPort(target, port):
	global s
	open_port = None
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)

	c = s.connect_ex((target, port))
	if c == 0:
		try:
		    data = banner(target ,port)
		    open_port = port
		    s.close()
		    
		except Exception as err:
		    print('' + target + '~Port: [open] ' + str(port, ))
		return open_port

def main():
	portrange = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
	for i in portrange:
		scan = threading.Thread(target=scanPort, args=(target, i))
		scan.start()   
		print("Heee: ",scan.get())

domain = 'markgacoka.com'
target = socket.gethostbyname(domain)
main()
print("--- %s seconds ---" % (time.time() - start_time))