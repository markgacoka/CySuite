import json
import requests

def crt_script(domain):
    CRT = []
    parameters = {"q": "%.{0}".format(domain), "output": "json"}
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
    try:
        res = requests.get("https://crt.sh/?", params=parameters, headers=headers, timeout=10)
        res.raise_for_status()

        if res.status_code == 200:
            data = json.loads(res.text)
            for d in data:
                if not d["name_value"].startswith("*"):
                    CRT.append(d["name_value"])
            return CRT
        return CRT
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
        
    return CRT