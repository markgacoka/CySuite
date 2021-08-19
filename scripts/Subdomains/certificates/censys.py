import re, os
import requests

def censys_script(domain):
    C = []
    API_URL = "https://www.censys.io/api/v1"
    UID = os.environ.get('CENSYS_UID')
    SECRET = os.environ.get('CENSYS_SECRET')

    if UID == "" or SECRET == "":
        print("  \__", "No Censys API credentials configured", "red")
        return []

    else:
        payload = {"query": domain}

        res = requests.post(API_URL + "/search/certificates", json=payload, auth=(UID, SECRET))

        if res.status_code == 429:
            print("  \__", "Rate limit exceeded. See https://www.censys.io/account for rate limit details.", "red")
            return C

        C = re.findall("CN=([\w\.\-\d]+)\." + domain, str(res.content))
        numberOfPages = re.findall("pages\":\s(\d+)?}", str(res.content))

        for page in range(2, int(numberOfPages[0]) + 1):
            payload = {"query": domain, "page": page}
            res = requests.post(API_URL + "/search/certificates", json=payload, auth=(UID, SECRET))
            tempC = re.findall("CN=([\w\.\-\d]+)\." + domain, str(res.content))
            C = C + tempC

        C = set(C)
        return C