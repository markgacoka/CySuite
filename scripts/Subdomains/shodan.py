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

def init(domain):
    subdomains, shodan = [], []
    SHODAN_API = os.environ.get('sQFwficu775PQ5QSvQCABwr0iTq3acxk')
    if SHODAN_API == "":
        print("  \__", "No Riddler API credentials configured")
        return []
    else:
        auth_response = requests.get('https://api.shodan.io/dns/domain/' + domain + '?key=' + SHODAN_API)
        data = json.loads(auth_response.text)
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
            shodan = set(shodan)
    return shodan

print(init('markgacoka.com'))
