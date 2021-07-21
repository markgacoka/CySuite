import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def init(domain):
    FSD = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    url = "https://findsubdomains.com/subdomains-of/{}".format(domain)
    response = requests.get(url, headers=headers, verify=False)
    print(response.text)
    name_soup = BeautifulSoup(response.text, "html.parser")
    for link in name_soup.findAll("a", {"class": "aggregated-link"}):
        try:
            if link.string is not None:
                FSD.append(link.string.strip())

        except KeyError as errk:
            print("  \__", errk)
            return []

    FSD = set(FSD)
    print("  \__ {0}: {1}".format("Unique subdomains found", len(FSD)))
    return FSD

print(init('markgacoka.com'))