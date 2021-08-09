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









