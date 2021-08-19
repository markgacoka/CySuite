import requests
from re import findall

def parseResponse(response, domain):
    try:
        token = response.split("\n]\n,[")[2].split("]\n")[0].split(",")[1].strip("\"")
        hostnameRegex = "([\w\.\-]+\.%s)" % (domain.replace(".", "\."))
        hosts = findall(hostnameRegex, response)
        return token, [host.lstrip(".") for host in hosts]
    except Exception:
        return "null", []

def google_transparency_script(domain):
    GTR = []
    baseURL = "https://www.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch"
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "referrer": "https://transparencyreport.google.com/https/certificates"}
    token = ""

    while True:
        if not token:
            url = "".join([baseURL, "?domain=", domain, "&include_expired=true&include_subdomains=true"])
        else:
            url = "".join([baseURL, "/page?domain=", domain, "&include_expired=true&include_subdomains=true&p=", token])
        response = requests.get(url, headers=headers)
        token, hostnames = parseResponse(response.text, domain)
        for hostname in hostnames:
            GTR.append(hostname)

        if token == "null":
            break

    GTR = set(GTR)
    return GTR