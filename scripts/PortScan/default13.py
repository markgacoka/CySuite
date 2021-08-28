# Threaded version of default12 (Advanced)
import socket
import threading

def check_socket_connection(host, port):
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.settimeout(5)
        result = server_sock.connect((host, port))
        print('[+] {}/tcp open'.format(port))
    except Exception as exception:
        print('[-] {}/tcp closed, Reason:{}'.format(port, (str(exception))))
    finally:
        server_sock.close()

def portScanner(host, ports):
    try:
        ip = socket.gethostbyname(host)
        print('[+] Scan Results for: ' + ip)
    except:
        print("[-] Cannot resolve {}: Unknown host".format(host))
        return
    for port in ports:
        t = threading.Thread(target=check_socket_connection, args=(ip, int(port)))
        t.start()

if __name__ == '__main__':
    remote_server = 'markgacoka.com'
    remote_server_ip = socket.gethostbyname(remote_server)
    ports = [i for i in range(100)]
    portScanner(remote_server, ports)