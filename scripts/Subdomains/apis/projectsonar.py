import requests
from json import loads

def filterDomain(domain, subdomains):
    domain_parts = domain.split(".")
    filtered = []
    for subdomain in subdomains:
        subdomain_parts = subdomain.split(".")

        if domain_parts == subdomain_parts[-1 * len(domain_parts):]:
            filtered.append(subdomain)

    return filtered

def projectsonar_script(domain):
    sonar = []
    url = "http://dns.bufferover.run/dns?q=.{0}".format(domain)
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    try:
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