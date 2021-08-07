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

# import textwrap
# import requests

# def print_roundtrip(response, *args, **kwargs):
#     format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
#     print(textwrap.dedent('''
#         ---------------- request ----------------
#         {req.method} {req.url}
#         {reqhdrs}

#         {req.body}
#         ---------------- response ----------------
#         {res.status_code} {res.reason} {res.url}
#         {reshdrs}

#         {res.text}
#     ''').format(
#         req=response.request, 
#         res=response, 
#         reqhdrs=format_headers(response.request.headers), 
#         reshdrs=format_headers(response.headers), 
#     ))

# url = 'https://markgacoka.com'
# req = requests.get(url, hooks={'response': print_roundtrip})
# print_roundtrip(req)

import requests, yarl

def insert_item(dic, item={}, pos=None):
    from collections import OrderedDict
    d = OrderedDict()
    if not item or not isinstance(item, dict):
        print('Aborting. Argument item must be a dictionary.')
        return dic
    if not pos:
        dic.update(item)
        return dic
    for item_k, item_v in item.items():
        for k, v in dic.items():
            if k == pos:
                d[item_k] = item_v
            d[k] = v
    return d

def send_request(request, url, method):
    data = {'username':'mark'}
    headers = {'User-Agent': request.META['HTTP_USER_AGENT']}
    payload = {}

    if method == 'GET':
        resp = requests.get(url, headers=headers, params=payload)
    elif method == 'POST':
        resp = requests.post(url, data=data, headers=headers)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers, params=payload)
    elif method == 'HEAD':
        resp = requests.head(url, headers=headers, params=payload)
    elif method =='OPTIONS':
        resp = requests.options(url, headers=headers, params=payload)
    elif method == 'PUT':
        resp = requests.put(url, data=data, headers=headers)
    else:
        return (None, None)

    response_headers = resp.headers
    request_headers = resp.request.headers
    full_url = yarl.URL(url)
    request_headers = insert_item(request_headers, {method: full_url.path_qs}, next(iter(request_headers)))
    request_headers = insert_item(request_headers, {'Host': url}, list(request_headers.keys())[1])
    return(request_headers, response_headers)









