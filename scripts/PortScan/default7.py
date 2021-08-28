# This script runs on Python 3
# Most likes on StackOverflow
import socket, threading

def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''

def scan_ports(host_ip, delay):
    threads = []        # To run TCP_connect concurrently
    output = {}         # For printing purposes

    for i in range(100):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output))
        threads.append(t)

    for i in range(100):
        threads[i].start()

    for i in range(100):
        threads[i].join()

    for i in range(100):
        if output[i] == 'Listening':
            print(str(i) + ': ' + output[i])

def main():
    target = 'markgacoka.com'
    host_ip = socket.gethostbyname(target)
    delay = 0.5
    scan_ports(host_ip, delay)

if __name__ == "__main__":
    main()