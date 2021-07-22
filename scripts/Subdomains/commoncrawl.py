import json, requests
IndexURL = "https://index.commoncrawl.org/collinfo.json"
indices = json.loads(requests.get(IndexURL).text)

target = 'markgacoka.com'
cc_urls = []
for index in indices:
    cc_urls.append(index['cdx-api'])

for url in cc_urls:
    print(requests.get(url + '?url=' + target + '&fl=url&matchType=domain&output=json').text)
