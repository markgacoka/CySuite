import json, threading

class PassiveDNS(EnumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        base_url = 'https://api.sublist3r.com/search.php?domain={domain}'
        self.engine_name = "PassiveDNS"
        self.lock = threading.Lock()
        self.q = q
        super(PassiveDNS, self).__init__(base_url, self.engine_name, domain, subdomains, q=q)
        return

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception as e:
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        if not resp:
            return self.subdomains

        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        try:
            subdomains = json.loads(resp)
            for subdomain in subdomains:
                if subdomain not in self.subdomains and subdomain != self.domain:
                    print("{0} : {1}".format(self.engine_name, subdomain))
                    self.subdomains.append(subdomain.strip())
        except Exception as e:
            pass