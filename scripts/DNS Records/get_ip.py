import tldextract
import ipaddress
import socket
import os, sys

def getIP(target):
    ext = tldextract.extract(target)
    domain = ext.registered_domain
    hostname = '.'.join(part for part in ext if part)

    try:
        ipaddress.ip_address(hostname)
        type_ip = True
        ip = hostname
        return ip
    except:
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception as e:
            return None

target = 'https://markgacoka.com'
print ('[+] Target : ' + target)
print(getIP(target))