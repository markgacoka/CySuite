import socket
import http.client as httplib
from http.client import responses
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def status_code(domain):
    try:
        if not domain.startswith('http://') and not domain.startswith('https://'):
            domain = 'http://' + domain
        req = Request(domain, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
        code = urlopen(req, timeout=10).getcode()
    except HTTPError as e:
        status = str(e.code) + ' ' + httplib.responses[e.code]
    except URLError as e:
        status = str(404) + ' ' + httplib.responses[404]
    except socket.timeout as e:
        status = str(400) + ' ' + httplib.responses[400]
    else:
        status = str(code) + ' ' + httplib.responses[code]
    yield status
