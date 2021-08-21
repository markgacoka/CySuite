import requests

def projectsonar_script2(domain):
    PS = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
    try:
        res = requests.get("https://sonar.omnisint.io/subdomains/" + domain, headers=headers, timeout=10)
        res.raise_for_status()
        stripped_response = res.text.strip().split()
        for res in stripped_response:
            res = res.replace('"', '')
            res = res.replace(',', '')
            PS.append(res)
        return PS[1:-1]
    except requests.exceptions.RequestException as err:
        print ("Request Exception:", err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    return []