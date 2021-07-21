from cfscrape import create_scraper
from bs4 import BeautifulSoup

def init(domain):
    dnsdb = []
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0"}
    url = "http://www.dnsdb.org/{0}/".format(domain)

    scrapper = create_scraper()
    response = scrapper.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.findAll("a"):
        try:
            if link.string is not None:
                dnsdb.append(link.string)

        except KeyError:
            pass

    dnsdb = set(dnsdb)
    print("  \__ {0}: {1}".format("Unique subdomains found", len(dnsdb)))
    return dnsdb

print(init('markgacoka.com'))