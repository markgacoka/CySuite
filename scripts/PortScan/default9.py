# WORKS!
# Total runtime:
import socket
import os

ports = 65535

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
for port in range(1, ports+1):
    con = check_port(target, port)
    if con == True:
        open.append(port)

print(open)