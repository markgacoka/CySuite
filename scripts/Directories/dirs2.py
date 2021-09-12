from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def scrape_links(domain):
    req = Request(domain, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")

    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    return(links)

url = 'https://markgacoka.com'
print(scrape_links(url))