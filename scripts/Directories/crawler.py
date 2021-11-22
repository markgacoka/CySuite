# Crawling, Passive sources (wayback), Databases (threat intelligence and web scrapers)

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class CrawlerTool:
    def __init__(self):
        self.internal_urls = set()
        self.external_urls = set()
        self.total_urls_visited = 0

    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_website_links(self, url):
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
            if not self.is_valid(href):
                continue
            if href in self.internal_urls:
                continue
            if domain_name not in href:
                if href not in self.external_urls:
                    self.external_urls.add(href)
                continue
            urls.add(href)
            if url[7:] in href:
                self.internal_urls.add(href)
        return urls

    def crawl(self, url, max_urls=30):
        """
        Crawls a web page and extracts all links.
        You'll find all links in `external_urls` and `internal_urls` global set variables.
        params:
            max_urls (int): number of max urls to crawl, default is 30.
        """
        global total_urls_visited
        self.total_urls_visited += 1
        links = self.get_all_website_links(url)
        for link in links:
            if self.total_urls_visited > max_urls:
                break
            self.crawl(link, max_urls=max_urls)

    def main_crawler(self, url):
        url = 'http://' +  url
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
            if urlopen(req, timeout=10).getcode() == 200:
                self.crawl(url)
            else:
                return [None, None, None]
        except:
            return [None, None, None]
        finally:
            return [len(self.external_urls) + len(self.internal_urls), list(self.internal_urls), list(self.external_urls)]

# [total number of links, [internal_links], [external_links]]
# _, inter, _ = main_crawler('blog.coda.io')
# print(inter)