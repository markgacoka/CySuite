import json
import requests

def openthreat_script(domain):
    OT = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
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