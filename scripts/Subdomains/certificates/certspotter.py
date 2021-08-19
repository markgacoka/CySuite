import requests
from re import findall

def parseResponse(response, domain):
    hostnameRegex = "([\w\.\-]+\.%s)" % (domain.replace(".", "\."))
    hosts = findall(hostnameRegex, str(response))
    return [host.lstrip(".") for host in hosts]

def certspotter_script(domain):
    CS = []

    base_url = "https://api.certspotter.com"
    next_link = "/v1/issuances?domain={0}&include_subdomains=true&expand=dns_names".format(domain)
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}

    while next_link:
        response = requests.get(base_url + next_link, headers=headers)
        if response.status_code == 429:
            print("  \__", "Search rate limit exceeded.")
            return []

        CS += parseResponse(response.content, domain)
        try:
            next_link = response.headers["Link"].split(";")[0][1:-1]
        except KeyError:
            break

    CS = set(CS)
    return CS