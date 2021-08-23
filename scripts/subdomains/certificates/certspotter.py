import requests
from re import findall
from fake_useragent import UserAgent

ua = UserAgent()

def parseResponse(response, domain):
    hostnameRegex = "([\w\.\-]+\.%s)" % (domain.replace(".", "\."))
    hosts = findall(hostnameRegex, str(response))
    return [host.lstrip(".") for host in hosts]

def certspotter_script(domain):
    CS = []

    base_url = "https://api.certspotter.com"
    next_link = "/v1/issuances?domain={0}&include_subdomains=true&expand=dns_names".format(domain)
    headers = {"User-Agent": ua.random}

    while next_link:
        try:
            res = requests.get(base_url + next_link, headers=headers, timeout=10)
            res.raise_for_status()
            if res.status_code == 429:
                break

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