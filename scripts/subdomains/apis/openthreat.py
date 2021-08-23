import json
import requests
from fake_useragent import UserAgent

ua = UserAgent()

def openthreat_script(domain):
    OT = []
    headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
    try:
        res = requests.get("https://otx.alienvault.com/otxapi/indicator/hostname/url_list/" + domain, headers=headers, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            data = json.loads(res.text)
            for d in data["url_list"]:
                OT.append(d["url"])
            return OT
        return []
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt) 
    return []