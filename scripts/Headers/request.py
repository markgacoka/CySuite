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

def send_request(request, url, method, data, auth, header):
    auth_arr = []
    headers, payload, params = {}, {}, {}

    full_url = yarl.URL(url)
    params = dict(full_url.query)
    if full_url.is_absolute() == False:
        return (None, None)
    
    origin = yarl.URL(url).origin()
    relative = yarl.URL(url).relative()
    path = yarl.URL(url).path
    
    headers['User-Agent'] = headers.get(request.META['HTTP_USER_AGENT'], 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
    if '' not in header:
        headers[header[0]] = headers.get(header[1], header[1])
    if data[0] != '':
         payload[data[0]] = payload.get(data[1], data[1])
    if auth[0] != '':
        auth_arr = auth

    if method == 'GET':
        if len(auth_arr) != 0:
            resp = requests.get(str(origin) + str(path), headers=headers, params=params, auth=(str(auth_arr[0]), str(auth_arr[1])))
        else:
            resp = requests.get(str(origin) + str(path), headers=headers, params=params)
    elif method == 'POST':
        if len(auth_arr) != 0:
            resp = requests.post(str(origin) + str(path), data=payload, headers=headers, auth=(str(auth_arr[0]), str(auth_arr[1])))
        else:
            resp = requests.post(str(origin) + str(path), data=payload, headers=headers)
    elif method == 'OPTIONS':
        resp = requests.options(str(origin) + str(path), headers=headers, params=params)
    elif method == 'HEAD':
        resp = requests.head(str(origin) + str(relative), headers=headers)
    elif method =='PUT':
        if len(auth_arr) != 0:
            resp = requests.put(str(origin) + str(path), data=payload, headers=headers, auth=(str(auth_arr[0]), str(auth_arr[1])))
        else:
            resp = requests.put(str(origin) + str(path), data=payload, headers=headers)
    elif method == 'DELETE':
        if len(auth_arr) != 0:
            resp = requests.delete(str(origin) + str(relative), headers=headers, auth=(str(auth_arr[0]), str(auth_arr[1])))
        else:
            resp = requests.delete(str(origin) + str(relative), data=payload, headers=headers)
    else:
        return (None, None)

    response_headers = resp.headers
    response_headers = {"Response ": str(resp.status_code) + ' ' + str(resp.reason), **response_headers}
    request_headers = resp.request.headers
    
    if (method == 'GET' or method == 'OPTIONS' or method == 'OPTIONS') and (full_url.path != '/'):
        request_headers = insert_item(request_headers, {method: full_url.relative}, next(iter(request_headers)))
    else:
        request_headers = insert_item(request_headers, {method: full_url.path}, next(iter(request_headers)))
    request_headers = insert_item(request_headers, {'Host': full_url.host}, list(request_headers.keys())[1])
    request_headers = insert_item(request_headers, payload)
    return(request_headers, response_headers)









