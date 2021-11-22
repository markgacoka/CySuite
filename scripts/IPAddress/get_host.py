import socket
import requests

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
    except Exception as e:
        ip = 'None'
    else:
       ip = ip
    yield ip