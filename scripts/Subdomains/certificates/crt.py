import json
import requests

def crt_script(domain):
    CRT = []
    parameters = {"q": "%.{0}".format(domain), "output": "json"}
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
    response = requests.get("https://crt.sh/?", params=parameters, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data:
            if not d["name_value"].startswith("*"):
                CRT.append(d["name_value"])

        CRT = set(CRT)
        return CRT

    else:
        print("  \__", "Something went wrong!")
        return []