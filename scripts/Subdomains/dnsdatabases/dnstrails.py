import requests, os
import json

def dnstrails_script(domain):
    DT = []
    DNSTrails_API_KEY = os.environ.get('DNSTRAILS_API_KEY')

    if DNSTrails_API_KEY == "":
        print("  \__", "No DNSTrails API key configured")
        return []

    else:
        headers = {'apikey': DNSTrails_API_KEY}
        url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(domain)
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            print("  \__", "You've exceeded the usage limits for your account.")
            return []
        else:
            payload = response.json()
        print(payload)

        DT = dict(payload.items())['subdomains']
        DT = set(DT)
        return DT