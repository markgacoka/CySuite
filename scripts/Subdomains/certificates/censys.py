import re, os
import requests

def censys_script(domain):
    C = []
    API_URL = "https://www.censys.io/api/v1"
    UID = os.environ.get('CENSYS_UID')
    SECRET = os.environ.get('CENSYS_SECRET')

    if UID == "" or SECRET == "":
        print("No Censys API credentials configured")
        return []

    else:
        payload = {"query": domain}
        try:
            res = requests.post(API_URL + "/search/certificates", json=payload, auth=(UID, SECRET), timeout=10)
            res.raise_for_status()

            if res.status_code == 200:
                C = re.findall("CN=([\w\.\-\d]+)\." + domain, str(res.content))
                numberOfPages = re.findall("pages\":\s(\d+)?}", str(res.content))

                for page in range(2, int(numberOfPages[0])):
                    payload = {"query": domain, "page": page}
                    res = requests.post(API_URL + "/search/certificates", json=payload, auth=(UID, SECRET))
                    tempC = re.findall("CN=([\w\.\-\d]+)\." + domain, str(res.content))
                    C = C + tempC

                C = set(C)
                return C
            else:
                return C
        except requests.exceptions.RequestException as err:
            print ("Request Exception:", err)
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)  