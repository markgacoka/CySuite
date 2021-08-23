import requests
from fake_useragent import UserAgent

ua = UserAgent()

def anubis_script(domain):
    anubis = []
    headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
    try:
        res = requests.get("https://jldc.me/anubis/subdomains/" + domain, headers=headers, timeout=10)
        res.raise_for_status()
        stripped_response = res.text.strip().split(",")
        for id, res in enumerate(stripped_response):
            res = res.replace('"', '')
            if id == 0:
                res = res[1:]
            if id == len(stripped_response)-1:
                res = res[:-1]
            anubis.append(res)
        return anubis
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt) 
    return []