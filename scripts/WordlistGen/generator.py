import requests, re
import urllib.request
from bs4 import BeautifulSoup

def extract_wordlist(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text().split()
    wordlist = set(filter(lambda x:x, map(lambda x:re.sub(r'[^A-Za-z]', '', x), text)))

    return wordlist 