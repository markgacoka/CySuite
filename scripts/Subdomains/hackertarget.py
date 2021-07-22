import requests
from urllib.parse import quote

def init(domain):
    HT = []
    url = "https://api.hackertarget.com/hostsearch/?q={0}".format(quote(domain))
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    response = requests.get(url, headers=headers).text
    hostnames = [result.split(",")[0] for result in response.split("\n")]

    for hostname in hostnames:
        if hostname:
            HT.append(hostname)

    HT = set(HT)
    print("  \__ {0}: {1}".format("Unique subdomains found", len(HT)))
    return HT

print(init('markgacoka.com'))