import socket

ports = 65535

def scanAllPorts(host):
    open = []
    for port in range(1, ports+1):
        if s.connect_ex((host, port)):
            pass
        else:
            open.append(port)
    return open

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
host = socket.gethostbyname('markgacoka.com')
print(host)
print(scanAllPorts(host))