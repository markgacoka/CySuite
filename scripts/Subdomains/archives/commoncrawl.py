#UNFINISHED
import json, requests

def commoncrawl_script(domain):
    IndexURL = "https://index.commoncrawl.org/collinfo.json"
    indices = json.loads(requests.get(IndexURL).text)

    cc_urls = []
    for index in indices:
        cc_urls.append(index['cdx-api'])

    for url in cc_urls:
        try:
            json_urls = requests.get(url + '?url=' + domain + '&fl=url&matchType=domain&output=json', timeout=10).text
            print(json_urls)
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        return []

