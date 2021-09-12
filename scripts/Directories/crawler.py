# Crawling, Passive sources (wayback), Databases (threat intelligence and web scrapers)

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

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
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser", from_encoding="iso-8859-1")
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
                external_urls.add(href)
            continue
        urls.add(href)
        if url[7:] in href:
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
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def main_crawler(url):
    url = 'http://' +  url
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
        if urlopen(req, timeout=10).getcode() == 200:
            crawl(url)
        else:
            return [None, None, None]
    except:
        return [None, None, None]
    finally:
        return [len(external_urls) + len(internal_urls), list(internal_urls), list(external_urls)]

# [total number of links, [internal_links], [external_links]]
# _, inter, _ = main_crawler('blog.coda.io')
# print(inter)