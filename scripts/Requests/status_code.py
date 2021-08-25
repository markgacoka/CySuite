import socket
import requests
import http.client as httplib
from http.client import responses, InvalidURL
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def status_code(domain):
    try:
        if domain.strip() == '':
            status = 'Not Applicable'
            yield status
        if not domain.startswith('http://') and not domain.startswith('https://'):
            domain = 'http://' + domain
        req = Request(domain, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
        code = urlopen(req, timeout=10).getcode()
    except HTTPError as e:
        status = str(e.code) + ' ' + httplib.responses[e.code]
    except InvalidURL:
        status = 'Not Applicable'
    except URLError as e:
        status = 'Not Applicable'
    except socket.timeout as e:
        status = str(200) + ' ' + httplib.responses[200]
    except requests.exceptions.Timeout:
        status = str(400) + ' ' + httplib.responses[400]
    else:
        status = str(code) + ' ' + httplib.responses[code]
    yield status
