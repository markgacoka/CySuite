from cfscrape import create_scraper
from bs4 import BeautifulSoup

def dnsdb_script(domain):
    dnsdb = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    url = "http://www.dnsdb.org/{0}/".format(domain)

    try:
        scrapper = create_scraper()
        response = scrapper.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.findAll("a"):
            if link.string is not None:
                dnsdb.append(link.string)
        return dnsdb
    except:
        print("An error occurred while scraping.")
    return []