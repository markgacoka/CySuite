import requests
import os

def passivetotal_script(domain):
    PT_USERNAME = os.environ.get('PT_USERNAME')
    PT_KEY = os.environ.get('PT_KEY')
    PT = []

    if PT_KEY == "" or PT_USERNAME == "":
        print("No PassiveTotal API credentials configured")
        return []
    else:
        auth = (PT_USERNAME, PT_KEY)
        url = "https://api.passivetotal.org/v2/enrichment/subdomains"
        data = {"query": domain}
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
        try:
            res = requests.get(url, auth=auth, json=data, headers=headers, timeout=10)
            res.raise_for_status()
            if res.status_code == 402:
                print("Quota exceeded.")
                return []

            for subdomain in res.json()["subdomains"]:
                PT.append("%s.%s" % (subdomain, domain))
            return PT
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        return PT