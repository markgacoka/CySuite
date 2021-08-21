import requests
from json import loads
from urllib.parse import quote

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
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
        try:
            res = requests.post(auth_url, json=auth, headers=headers, timeout=10)
            res.raise_for_status()
            res_json = loads(res.text)

            if res_json["meta"]["code"] == 200:
                auth_token = res_json["response"]["user"]["authentication_token"]
                search = {"query": "pld:{0}".format(quote(domain)), "output": "host"}
                search_url = "https://riddler.io/api/search"
                headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json", "authentication-token": auth_token}
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