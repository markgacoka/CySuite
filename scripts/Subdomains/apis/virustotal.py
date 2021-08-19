import requests, os

def virustotal_script(domain):
    VT = []
    VT_API_KEY = os.environ.get('VT_API_KEY_FREE')

    if VT_API_KEY == "":
        print("  \__", "No VirusTotal API key configured", "red")
        return []
    else:
        parameters = {"domain": domain, "apikey": VT_API_KEY}
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
        response = requests.get("https://www.virustotal.com/vtapi/v2/domain/report", params=parameters, headers=headers)
        response_dict = response.json()

        if "subdomains" in response_dict:
            for sd in response_dict["subdomains"]:
                VT.append(sd)

        VT = set(VT)
        print("  \__ {0}: {1}".format("Unique subdomains found", len(VT)))
        return VT