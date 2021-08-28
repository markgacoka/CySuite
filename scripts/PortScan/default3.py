import socket
# Short and simple but doesn't work

import sys

ports = 65535

def portscan(target):
    try:
        for port in range(1, ports+1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target, port))

            if (result == 0):
                print(f"Port {port} open")
            
            else:
                print(f"Port {port} closed")
            s.close()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()

    except socket.gaierror:
        print("The hostname couldn't be resolved.")
        sys.exit()

    except socket.error:
        print("Couldn't connect to the server.")
        sys.exit()

url = 'google.com'
portscan(url)
    