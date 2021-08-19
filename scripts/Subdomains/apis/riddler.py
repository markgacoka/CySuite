import requests
from json import loads
from urllib.parse import quote

def riddler_script(domain):
    riddler = []
    RIDDLER_USERNAME = ''
    RIDDLER_PASSWORD = ''
    if RIDDLER_USERNAME == "" or RIDDLER_PASSWORD == "":
        print("  \__", "No Riddler API credentials configured")
        return []
    else:
        auth = {"email": RIDDLER_USERNAME, "password": RIDDLER_PASSWORD}
        auth_url = "https://riddler.io/auth/login"
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
        auth_response = requests.post(auth_url, json=auth, headers=headers)
        auth_response_json = loads(auth_response.text)

        if auth_response_json["meta"]["code"] == 200:
            auth_token = auth_response_json["response"]["user"]["authentication_token"]
            search = {"query": "pld:{0}".format(quote(domain)), "output": "host"}
            search_url = "https://riddler.io/api/search"
            headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json", "authentication-token": auth_token}
            search_response = requests.post(search_url, json=search, headers=headers)
            if search_response.status_code == 500:
                print("  \__", "Internal Server Error.")
                return riddler

            else:
                search_response_json = loads(search_response.text)

            for item in search_response_json:
                riddler.append(item["host"])

            riddler = set(riddler)
            return riddler
        else:
            print("  \__", "Invalid Riddler API credentials.")
            return []