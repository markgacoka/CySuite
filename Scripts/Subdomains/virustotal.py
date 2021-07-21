import requests

def init(domain):
    VT = []
    VT_API_KEY = '1c8636990364fc0922d77c4d748f5711716aebcc451ce4eca9c50c759374a080'

    if VT_API_KEY == "":
        print("  \__", colored("No VirusTotal API key configured", "red"))
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

print(init('markgacoka.com'))