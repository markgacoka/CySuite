# Can be installed locally using NPM
# Current implementation is a webapp on appspot
import requests

BASE = 'https://render-tron.appspot.com/screenshot/'
url = 'https://google.com'
path = 'target.jpg'
response = requests.get(BASE + url, stream=True)
if response.status_code == 200:
    with open(path, 'wb') as file:
        for chunk in response:
            file.write(chunk)