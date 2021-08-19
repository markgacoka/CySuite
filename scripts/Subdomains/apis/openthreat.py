import json
import requests

def openthreat_script(domain):
    OT = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
    response = requests.get("https://otx.alienvault.com/otxapi/indicator/hostname/url_list/" + domain, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data["url_list"]:
            OT.append(d["url"])

        OT = set(OT)
        return OT
    else:
        print("  \__", "Something went wrong!")
        return []