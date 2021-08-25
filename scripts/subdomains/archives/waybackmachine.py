import requests
from urllib.parse import quote
from urllib.parse import urlparse

def waybackmachine_script(domain):
    WB = []
    url = "http://web.archive.org/cdx/search/cdx?url=*.{0}&output=json&fl=original&collapse=urlkey".format(quote(domain))
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        urls = res.json()

        for url in urls:
            urlString = url[0]
            if domain in urlString:
                parsed_uri = urlparse(urlString)
                onlyDomain = "{uri.netloc}".format(uri=parsed_uri).split(":")[0]
                WB.append(onlyDomain)
            else:
                pass
        return WB
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    return WB
       