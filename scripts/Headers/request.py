# import requests

# def pretty_print_POST(req):
#     print('{}\r\n{}\r\n\r\n{}'.format(
#         req.method + ' ' + req.url,
#         '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
#         req.body,
#     ))

# url = 'https://markgacoka.com'
# headers = {'X-Custom':'Test'}
# data = 'a=1&b=2'
# req = requests.Request('POST', url, headers=headers, data=data)
# prepared = req.prepare()
# pretty_print_POST(prepared)

# import requests

# response = requests.post('http://httpbin.org/post', data={'key1':'value1'})
# print(response.request.url)
# print(response.request.body)
# print(response.request.headers)

# import requests
# import http.client as httplib

# def patch_send():
#     old_send= httplib.HTTPConnection.send
#     def new_send( self, data ):
#         print(data)
#         return old_send(self, data)
#     httplib.HTTPConnection.send= new_send

# patch_send()
# requests.get("http://www.python.org")

import textwrap
import requests

def print_roundtrip(response, *args, **kwargs):
    format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {reqhdrs}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        {res.text}
    ''').format(
        req=response.request, 
        res=response, 
        reqhdrs=format_headers(response.request.headers), 
        reshdrs=format_headers(response.headers), 
    ))

url = 'https://markgacoka.com'
requests.get(url, hooks={'response': print_roundtrip})