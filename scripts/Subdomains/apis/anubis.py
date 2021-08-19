import requests

def anubis_script(domain):
    anubis = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "content-type": "application/json"}
    response = requests.get("https://jldc.me/anubis/subdomains/" + domain, headers=headers)
    stripped_response = response.text.strip().split(",")
    for id, response in enumerate(stripped_response):
        response = response.replace('"', '')
        if id == 0:
            response = response[1:]
        if id == len(stripped_response)-1:
            response = response[:-1]
        anubis.append(response)
    return anubis