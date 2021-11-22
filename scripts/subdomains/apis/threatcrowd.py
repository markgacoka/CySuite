import json
import requests

def threatcrowd_script(domain):
    TC = []
    try:
        res = requests.get("https://www.threatcrowd.org/searchApi/v2/domain/report/", params={"domain": domain}, timeout=10)
        res.raise_for_status()
        response = json.loads(res.text)
        resp_code = int(response["response_code"])
        if resp_code == 1:
            for sd in response["subdomains"]:
                TC.append(sd)
        return TC
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    return []