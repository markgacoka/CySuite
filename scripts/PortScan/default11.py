# Slow, never runs!
from socket import * 

if __name__ == '__main__':
    target = 'markgacoka.com'
    targetIP = gethostbyname(target)
    print('Starting scan on host ', targetIP)

    for i in range(20, 1025):
        s = socket(AF_INET, SOCK_STREAM)
        result = s.connect_ex((targetIP, i))
        if(result == 0) :
            print('Port %d: OPEN' % (i,))
        s.close()