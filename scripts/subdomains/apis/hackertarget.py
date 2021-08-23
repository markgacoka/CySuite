import requests
from urllib.parse import quote
from fake_useragent import UserAgent

ua = UserAgent()

def hackertarget_script(domain):
    HT = []
    url = "https://api.hackertarget.com/hostsearch/?q={0}".format(quote(domain))
    headers = {"user-agent": ua.random}
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        hostnames = [result.split(",")[0] for result in res.split("\n")]

        for hostname in hostnames:
            if hostname:
                HT.append(hostname)
        return HT
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt) 
    return []