from bs4 import BeautifulSoup
import requests

def scrape_links(domain):
    page = requests.get(domain)    
    data = page.text
    soup = BeautifulSoup(data, "lxml")

    links = []
    for link in soup.findAll('a'):
        if link.get('href').startswith('/'):
            links.append(domain + link.get('href'))
        else:
            links.append(link.get('href'))

    return(links)

url = 'https://markgacoka.com'
print(scrape_links(url))