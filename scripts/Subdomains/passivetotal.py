import requests

def init(domain):
    PT_KEY = ''
    PT_SECRET = ''

    if PT_KEY == "" or PT_SECRET == "":
        print("  \__", "No PassiveTotal API credentials configured")
        return []
    else:
        auth = (PT_KEY, PT_SECRET)
        url = "https://api.passivetotal.org/v2/enrichment/subdomains"
        data = {"query": domain}
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
        response = requests.get(url, auth=auth, json=data, headers=headers)

        if response.status_code == 402:
            print("  \__", "Quota exceeded.")
            return []

        try:
            for subdomain in response.json()["subdomains"]:
                PT.append("%s.%s" % (subdomain, domain))

            PT = set(PT)

            print("  \__ {0}: {1}".format("Unique subdomains found", len(PT)))
            return PT

        except KeyError as errk:
            print("  \__", errk)
            return []

print(init('markgacoka.com'))