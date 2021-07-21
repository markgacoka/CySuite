import json
import requests

def init(domain):
    TC = []
    result = requests.get("https://www.threatcrowd.org/searchApi/v2/domain/report/", params={"domain": domain})
    try:
        RES = json.loads(result.text)
        resp_code = int(RES["response_code"])
        if resp_code == 1:
            for sd in RES["subdomains"]:
                TC.append(sd)
        TC = set(TC)
        print("  \__ {0}: {1}".format("Unique subdomains found", len(TC)))
        return TC

    except ValueError as errv:
        print("  \__", errv)
        return []

print(init('markgacoka.com'))