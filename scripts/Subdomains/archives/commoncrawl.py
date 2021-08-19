import json, requests

def commoncrawl_script(domain):
    IndexURL = "https://index.commoncrawl.org/collinfo.json"
    indices = json.loads(requests.get(IndexURL).text)

    cc_urls = []
    for index in indices:
        cc_urls.append(index['cdx-api'])

    for url in cc_urls:
        json_urls = requests.get(url + '?url=' + domain + '&fl=url&matchType=domain&output=json').text
        print("\n\nNEW")
        print(json_urls)

