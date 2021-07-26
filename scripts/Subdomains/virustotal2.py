import threading, os

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