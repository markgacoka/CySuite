import requests

def init(domain):
    DT = []
    DNSTrails_API_KEY = 'FK78Fbzl4m7wdwoyoVigvdcjrCzoI1yZ'

    if DNSTrails_API_KEY == "":
        print("  \__", "No DNSTrails API key configured")
        return []

    else:
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json", "APIKEY": DNSTrails_API_KEY}
        url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(domain)
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            print("  \__", "You've exceeded the usage limits for your account.")
            return []
        else:
            payload = response.json()

        DT = dict(payload.items())['subdomains']
        DT = set(DT)
        print("  \__ {0}: {1}".format("Unique subdomains found", len(DT)))
        return DT

print(init('coda.io'))