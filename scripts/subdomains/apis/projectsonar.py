import requests
import random
from json import loads

def filterDomain(domain, subdomains):
    domain_parts = domain.split(".")
    filtered = []
    for subdomain in subdomains:
        subdomain_parts = subdomain.split(".")

        if domain_parts == subdomain_parts[-1 * len(domain_parts):]:
            filtered.append(subdomain)

    return filtered

def GET_UA():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
        ]
 
    return random.choice(uastrings)

def projectsonar_script(domain):
    sonar = []
    url = "http://dns.bufferover.run/dns?q=.{0}".format(domain)
    try:
        headers = {"User-Agent": GET_UA()}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        response_json = loads(res.text)

        if response_json["FDNS_A"]:
            for record in response_json["FDNS_A"]:
                sonar += record.split(",")

        if response_json["RDNS"]:
            for record in response_json["RDNS"]:
                sonar.append(record.split(",")[1])

        sonar = filterDomain(domain, set([subdomain.lower() for subdomain in sonar]))
        return sonar
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt) 
    return []