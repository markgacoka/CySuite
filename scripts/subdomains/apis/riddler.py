import requests
import random
from json import loads
from urllib.parse import quote

def GET_UA():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
        ]
 
    return random.choice(uastrings)

def riddler_script(domain):
    riddler = []
    RIDDLER_USERNAME = ''
    RIDDLER_PASSWORD = ''
    if RIDDLER_USERNAME == "" or RIDDLER_PASSWORD == "":
        print("No Riddler API credentials configured")
        return []
    else:
        auth = {"email": RIDDLER_USERNAME, "password": RIDDLER_PASSWORD}
        auth_url = "https://riddler.io/auth/login"
        headers = {"User-Agent": GET_UA()}
        try:
            res = requests.post(auth_url, json=auth, headers=headers, timeout=10)
            res.raise_for_status()
            res_json = loads(res.text)

            if res_json["meta"]["code"] == 200:
                auth_token = res_json["response"]["user"]["authentication_token"]
                search = {"query": "pld:{0}".format(quote(domain)), "output": "host"}
                search_url = "https://riddler.io/api/search"
                headers = {"user-agent": ua.random, "Content-Type": "application/json", "Authentication-Token": auth_token}
                search_response = requests.post(search_url, json=search, headers=headers)
                if search_response.status_code == 200:
                    search_response_json = loads(search_response.text)
                else:
                    print("An error occurred.")
                    return riddler

                for item in search_response_json:
                    riddler.append(item["host"])
                return riddler
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt) 
        return []