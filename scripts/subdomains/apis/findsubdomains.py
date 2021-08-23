import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent

ua = UserAgent()

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def findsubdomains_script(domain):
    FSD = []
    headers = {"User-Agent": ua.random}
    url = "https://findsubdomains.com/subdomains-of/{}".format(domain)
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=10)
        res.raise_for_status()
        name_soup = BeautifulSoup(res.text, "html.parser")
        for link in name_soup.findAll("a", {"class": "aggregated-link"}):
            try:
                if link.string is not None:
                    FSD.append(link.string.strip())
            except KeyError as errk:
                print(errk)
                return []
        return FSD
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt) 
    return []