import socket
import requests

def get_web_details(domain_lst):
    return_lst = []
    for domain in domain_lst:
        try:
            return_lst.append(socket.gethostbyname(domain))
        except:
            return_lst.append('None')
    return return_lst