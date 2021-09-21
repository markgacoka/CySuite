# Can be installed locally using NPM
# Current implementation is a webapp on appspot
import os
import requests

def take_screenshot(url):
    BASE = 'https://render-tron.appspot.com/screenshot/'
    path = os.getcwd() + '/media/screenshots/{}.jpg'.format(url)
    full_url = 'http://' + url
    response = requests.get(BASE + full_url, stream=True)
    try:
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)
        else:
            return False
    except:
        return False
    else:
        return True