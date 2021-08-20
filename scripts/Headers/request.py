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
    headers = {}
    payload = {}
    auth_arr = []
    params = {}
    full_url = yarl.URL(url)

    headers['User-Agent'] = headers.get(request.META['HTTP_USER_AGENT'], 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
    headers[header[0]] = headers.get(header[1], header[1])
    if data[0] != '':
         payload = data
    if auth[0] != '':
        auth_arr = auth
    if full_url.query_string != '':
        queries = full_url.query_string.split('&')
        for query in queries:
            query_part = query.split('=')
            params[query_part[0]] = query_part[1]

    params = dict(full_url.query)

    print(headers)
    print(payload)
    print(auth_arr)
    print(full_url.parent)

    if method == 'GET':
        # headers | no payload | auth_dict | params
        if len(auth_arr) != 0:
            resp = requests.get(url, headers=headers, params=params, auth=(str(auth_arr[0]), str(auth_arr[1])))
        else:
            resp = requests.get(url, headers=headers, params=params)
        print(resp.status_code)
    elif method == 'POST':
        resp = requests.post(url, data=payload, headers=headers)
    elif method == 'OPTIONS':
        resp = requests.options(url, headers=headers, params=payload)
    elif method == 'HEAD':
        resp = requests.head(url, headers=headers, params=payload)
    elif method =='PUT':
        resp = requests.put(url, headers=headers, data=payload, params=payload)
    elif method == 'DELETE':
        resp = requests.delete(url, data=payload, headers=headers)
    else:
        return (None, None)

    response_headers = resp.headers
    request_headers = resp.request.headers
    
    request_headers = insert_item(request_headers, {method: full_url.path_qs}, next(iter(request_headers)))
    request_headers = insert_item(request_headers, {'Host': full_url.host}, list(request_headers.keys())[1])
    return(request_headers, response_headers)









