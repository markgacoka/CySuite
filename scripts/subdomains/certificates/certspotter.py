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
        try:
            res = requests.get(base_url + next_link, headers=headers, timeout=10)
            res.raise_for_status()
            if res.status_code == 429:
                print("Search rate limit exceeded.")
                return []

            CS += parseResponse(res.content, domain)
            try:
                next_link = res.headers["Link"].split(";")[0][1:-1]
            except KeyError:
                break
            return CS
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
    return CS