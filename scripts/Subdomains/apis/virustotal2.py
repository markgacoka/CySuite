import os
import threading
import multiprocessing
import requests
import urllib.parse as urlparse

class EnumratorBase(object):
    def __init__(self, base_url, engine_name, domain, subdomains=None):
        subdomains = subdomains or []
        self.domain = urlparse.urlparse(domain).netloc
        self.session = requests.Session()
        self.subdomains = []
        self.timeout = 25
        self.base_url = base_url
        self.engine_name = engine_name
        self.headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.8',
              'Accept-Encoding': 'gzip',
          }

    def print_(self, text):
        return

    def send_req(self, query, page_no=1):
        
        url = self.base_url.format(query=query, page_no=page_no)
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return self.get_response(resp)

    def get_response(self, response):
        if response is None:
            return 0
        return response.text if hasattr(response, "text") else response.content

    def check_max_subdomains(self, count):
        if self.MAX_DOMAINS == 0:
            return False
        return count >= self.MAX_DOMAINS

    def check_max_pages(self, num):
        if self.MAX_PAGES == 0:
            return False
        return num >= self.MAX_PAGES

    # override
    def extract_domains(self, resp):
        """ chlid class should override this function """
        return

    # override
    def check_response_errors(self, resp):
        """ chlid class should override this function
        The function should return True if there are no errors and False otherwise
        """
        return True

    def should_sleep(self):
        """Some enumrators require sleeping to avoid bot detections like Google enumerator"""
        return

    def generate_query(self):
        """ chlid class should override this function """
        return

    def get_page(self, num):
        """ chlid class that user different pagnation counter should override this function """
        return num + 10

    def enumerate(self, altquery=False):
        flag = True
        page_no = 0
        prev_links = []
        retries = 0

        while flag:
            query = self.generate_query()
            if(query):
                count = query.count(self.domain)  # finding the number of subdomains found so far
            else:
                count = 0
                
            # if they we reached the maximum number of subdomains in search query
            # then we should go over the pages
            if self.check_max_subdomains(count):
                page_no = self.get_page(page_no)

            if self.check_max_pages(page_no):  # maximum pages for Google to avoid getting blocked
                return self.subdomains
            resp = self.send_req(query, page_no)

            # check if there is any error occured
            if not self.check_response_errors(resp):
                return self.subdomains
            links = self.extract_domains(resp)

            # if the previous page hyperlinks was the similar to the current one, then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)

        # make another retry maybe it isn't the last page
                if retries >= 3:
                    return self.subdomains

            prev_links = links
            self.should_sleep()

        return self.subdomains


class EnumratorBaseThreaded(multiprocessing.Process, EnumratorBase):
    def __init__(self, base_url, engine_name, domain, subdomains=None, q=None, lock=threading.Lock()):
        subdomains = subdomains or []
        EnumratorBase.__init__(self, base_url, engine_name, domain, subdomains)
        multiprocessing.Process.__init__(self)
        self.lock = lock
        self.q = q
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)

class Virustotal(EnumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        base_url = "https://www.virustotal.com/gui/domain/{domain}/details"
        self.apiurl = 'https://www.virustotal.com/vtapi/v2/domain/report'
        self.API_KEY= os.environ.get('VT_API_KEY_PAID'),
        self.params =  {'apikey':self.API_KEY,'domain':domain}
        self.engine_name = "Virustotal"
        self.lock = threading.Lock()
        self.q = q
        super(Virustotal, self).__init__(base_url, self.engine_name, domain, subdomains, q=q)
        return

    # the main send_req need to be rewritten
    def send_req(self, url):
        try:
            resp = self.session.get(self.apiurl, headers=self.headers, params=self.params)
        except Exception as e:
            print(e)
            resp = None
        else:
            return resp.json()

    # once the send_req is rewritten we don't need to call this function, the stock one should be ok
    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.send_req(url)
        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        try:
            subdomains = resp.get('subdomains')
            for subdomain in subdomains:
                self.subdomains.append(subdomain.strip())
        except Exception as e:
            print(e)
            pass