import requests, sys, json, os

def sorter(subdomains):
    local, final = [], []
    for item in subdomains:
        reversed_sub = ".".join(str(item).split('.')[::-1])
        local.append(reversed_sub)

    sortedlist = sorted(local)
    for item in sortedlist:
        d_reversed_sub = ".".join(str(item).split('.')[::-1])
        final.append(d_reversed_sub)
    return final

def shodan_script(domain):
    subdomains, shodan = [], []
    SHODAN_API = os.environ.get('SHODAN_API_KEY')
    if SHODAN_API == "":
        print("  \__", "No Riddler API credentials configured")
        return []
    else:
        try:
            res = requests.get('https://api.shodan.io/dns/domain/' + domain + '?key=' + SHODAN_API, timeout=10)
            res.raise_for_status()
            data = json.loads(res.text)
            if 'error' in data:
                shodan = []
            else:
                for item in data["data"]:
                    entry = item["subdomain"]  
                    record_type = item["type"]
                    value = item["value"]
                    if record_type == 'CNAME' and domain in value: 
                        delim = value.split('.')
                        match = delim[-2] + '.' + delim[-1]
                        if match == domain:
                            subdomains.add(value)

                for url in sorter(subdomains): 
                    shodan.append(url)
            return shodan
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt) 
        return []
