# Crawling, Passive sources (wayback), Databases (threat intelligence and web scrapers)
 
# from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen

# def scrape_links(domain):
#     req = Request(domain, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
#     html_page = urlopen(req)
#     soup = BeautifulSoup(html_page, "lxml")

#     links = []
#     for link in soup.findAll('a'):
#         links.append(link.get('href'))

#     return(links)

# url = 'https://markgacoka.com'
# print(scrape_links(url))

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

internal_urls = set()
external_urls = set()

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                print(f"[!] External link: {href}")
                external_urls.add(href)
            continue
        print(f"[*] Internal link: {href}")
        urls.add(href)
        internal_urls.add(href)
    return urls

total_urls_visited = 0
def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"[*] Crawling: {url}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

if __name__ == "__main__":
    url = 'https://markgacoka.com'
    crawl(url)
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))