import requests
from http.client import responses

def url_status(url):
    response = requests.get(url)
    return str(response.status_code) + ' ' + responses[response.status_code]