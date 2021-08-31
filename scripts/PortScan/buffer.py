import pycurl
from io import BytesIO
from http.client import responses

url = 'http://markgacoka.com'
c = pycurl.Curl()
e = BytesIO()
c.setopt(pycurl.URL, url)
c.setopt(pycurl.HEADER, True)
c.setopt(pycurl.NOBODY, True)
c.setopt(pycurl.WRITEFUNCTION, e.write)
c.perform()

print(e.getvalue().decode('UTF-8'))
print()
c.close()