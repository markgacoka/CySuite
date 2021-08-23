import requests, os
from fake_useragent import UserAgent

ua = UserAgent()

def virustotal_script(domain):
    VT = []
    VT_API_KEY = os.environ.get('VT_API_KEY_FREE')

    if VT_API_KEY == "":
        print("No VirusTotal API key configured", "red")
        return []
    else:
        parameters = {"domain": domain, "apikey": VT_API_KEY}
        headers = {"User-Agent": ua.random}
        try:
            res = requests.get("https://www.virustotal.com/vtapi/v2/domain/report", params=parameters, headers=headers, timeout=10)
            res.raise_for_status()
            response_dict = res.json()
            if "subdomains" in response_dict:
                for sd in response_dict["subdomains"]:
                    VT.append(sd)
            return VT
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        return []