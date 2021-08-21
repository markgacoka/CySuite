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
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            token, hostnames = parseResponse(res.text, domain)
            for hostname in hostnames:
                GTR.append(hostname)
            if token == "null":
                break
            return GTR
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)

    return GTR