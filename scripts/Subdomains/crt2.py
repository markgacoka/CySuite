import threading
import re

class CrtSearch(EnumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        base_url = 'https://crt.sh/?q={domain}'
        self.domain = domain
        self.queryurl = 'https://crt.sh/?q={0}&output=json'.format(self.domain)
        self.engine_name = "SSL Certificates"
        self.lock = threading.Lock()
        self.q = q
        super(CrtSearch, self).__init__(base_url, self.engine_name, domain, subdomains, q=q)
        return

    def req(self, url):
        try:
            resp = self.session.get(self.queryurl, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        if resp:
            self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        link_regx = re.compile('<TD>(.*?)</TD>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                subdomain = link.strip()
                
                #print("SUBDOMAINS ", subdomain)
                if(self.domain in subdomain and "</A>" not in subdomain):
                    if not subdomain.endswith(self.domain) or '*' in subdomain:
                        continue

                    if '@' in subdomain:
                        subdomain = subdomain[subdomain.find('@')+1:]

                    if subdomain not in self.subdomains and subdomain != self.domain:
                        print("{0} : {1}".format(self.engine_name, subdomain))
                        self.subdomains.append(subdomain.strip())
                        
        except Exception as e:
            pass