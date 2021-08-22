import socket
import requests

def get_ip():
    domain = yield
    try:
        ip = socket.gethostbyname(domain)
    except Exception as e:
        ip = 'None'
    else:
       pass
    yield ip