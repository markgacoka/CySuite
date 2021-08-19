import requests

def projectsonar_script2(domain):
    PS = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
    response = requests.get("https://sonar.omnisint.io/subdomains/" + domain, headers=headers)
    stripped_response = response.text.strip().split()
    for response in stripped_response:
        response = response.replace('"', '')
        response = response.replace(',', '')
        PS.append(response)
    return PS[1:-1]