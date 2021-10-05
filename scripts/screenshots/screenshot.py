# Can be installed locally using NPM
# Current implementation is a webapp on appspot
import os
import requests
import urllib.request
import boto3
import http.client as httplib
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

def get_status_code(host):
    full_url_1 = 'http://' + host
    full_url_2 = 'https://' + host
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "Content-Type": "application/json"}
    try:
        r1 = requests.head(full_url_1, headers=headers, allow_redirects=True, verify=False).status_code
        r2 = requests.head(full_url_2, headers=headers, allow_redirects=True, verify=False).status_code
        if r1 == 200 or r2 == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False
    else:
        return False

def upload_screenshot(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0", "Content-Type": "application/json"}
    s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'))
    BASE = 'https://render-tron.appspot.com/screenshot/'
    full_url = 'http://' + url
    data = requests.get(BASE + full_url, headers=headers, stream=True).content
    bucket = s3.Bucket(name="cysuite-bucket")
    bucket.upload_fileobj(BytesIO(data), 'media/screenshot/{}.jpg'.format(url))
    return 'https://cysuite-bucket.s3.us-west-2.amazonaws.com/media/screenshot/' + url + '.jpg'