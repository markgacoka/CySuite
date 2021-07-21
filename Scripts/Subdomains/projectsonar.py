import requests
from json import loads

def uniqueList(subdomains):
    uniqe_subdomains = set()
    for subdomain in subdomains:
        uniqe_subdomains.add(subdomain.lower())

    return list(uniqe_subdomains)


def filterDomain(domain, subdomains):
    domain_parts = domain.split(".")
    filtered = []
    for subdomain in subdomains:
        subdomain_parts = subdomain.split(".")

        if domain_parts == subdomain_parts[-1 * len(domain_parts):]:
            filtered.append(subdomain)

    return filtered

def init(domain):
    sonar = []
    url = "http://dns.bufferover.run/dns?q=.{0}".format(domain)
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    response = requests.get(url, headers=headers)
    response_json = loads(response.text)

    if response_json["FDNS_A"]:
        for record in response_json["FDNS_A"]:
            sonar += record.split(",")

    if response_json["RDNS"]:
        for record in response_json["RDNS"]:
            sonar.append(record.split(",")[1])

    sonar = filterDomain(domain, uniqueList(sonar))

    print("  \__ {0}: {1}".format("Unique subdomains found", len(sonar)))
    return sonar

print(init('markgacoka.com'))