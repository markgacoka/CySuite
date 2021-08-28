# WORKS!
# Total runtime: 9.639406204223633 seconds
import socket
import time
start_time = time.time()

DEFAULT_TIMEOUT = 0.5
SUCCESS = 0
def check_port(*host_port, timeout=DEFAULT_TIMEOUT):
    # Create and configure the socket.
    sock = socket.socket()
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connected = sock.connect_ex(host_port) is SUCCESS
    sock.close()
    return connected

open = []
target = 'markgacoka.com'
portrange = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]# top 20
for port in portrange:
    con = check_port(target, port)
    if con == True:
        open.append(port)

print(open)
print("--- %s seconds ---" % (time.time() - start_time))