import json, threading

class ThreatCrowd(EnumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        base_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}'
        self.domain = domain 
        self.queryurl = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={0}'.format(self.domain)
        self.engine_name = "ThreatCrowd"
        self.lock = threading.Lock()
        self.q = q
        super(ThreatCrowd, self).__init__(base_url, self.engine_name, domain, subdomains, q=q)
        return

    def req(self, url):
        try:
            resp = self.session.get(self.queryurl, headers=self.headers, timeout=self.timeout)
        except Exception as e:
            print("ERROR ", e)
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        try:
            links = json.loads(resp)['subdomains']
            for link in links:
                subdomain = link.strip()
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain not in self.subdomains and subdomain != self.domain:
                    print("{0} : {1}".format(self.engine_name, subdomain))
                    self.subdomains.append(subdomain.strip())
        except Exception as e:
            pass