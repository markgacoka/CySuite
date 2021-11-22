import requests, os
import json

def dnstrails_script(domain):
    DT = []
    DNSTrails_API_KEY = os.environ.get('DNSTRAILS_API_KEY')

    if DNSTrails_API_KEY == "":
        print("No DNSTrails API key configured")
        return []
    else:
        headers = {'apikey': DNSTrails_API_KEY}
        url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(domain)
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            if response.status_code == 429:
                print("  \__", "You've exceeded the usage limits for your account.")
                return []
            else:
                payload = res.json()

            DT = dict(payload.items())['subdomains']
            return DT
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)