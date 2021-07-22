import re
import requests

def init(domain):
    C = []
    API_URL = "https://www.censys.io/api/v1"
    UID = 'c4a9c678-dd3b-4b20-af47-610374f2fe89'
    SECRET = 'c9ZkXNOkSRK6O06e6EUGhk5vQnEogyo8'

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

        print("  \__ {0}: {1}".format("Unique subdomains found", len(C)))
        return C

print(init('markgacoka.com'))