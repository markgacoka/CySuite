import requests

response = requests.get("https://markgacoka.com")
for header, value in response.headers.items():
    print(header, ": ", value)