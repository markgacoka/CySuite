import requests
from re import findall
from json import loads

def parseSubject(subject, domain):
    hostnameRegex = "([\w\.\-]+\.%s)" % (domain.replace(".", "\."))
    hosts = findall(hostnameRegex, subject)
    return [host.lstrip(".") for host in hosts]

def entrust_certificates_script(domain):
    ENT = []
    url = "https://ctsearch.entrust.com/api/v1/certificates?fields=subjectDN&domain={0}&includeExpired=true&exactMatch=false&limit=5000".format(domain)
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        response_json = loads(res.text.replace("\\u003d", "="))

        for item in response_json:
            ENT += parseSubject(item["subjectDN"], domain)
        return ENT
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    return ENT