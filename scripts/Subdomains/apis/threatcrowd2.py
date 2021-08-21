import json
import multiprocessing
import urllib.parse as urlparse

import sys
sys.path.append('../search_engines')
from utils import enumeratorBaseThreaded

class ThreatCrowd(enumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        base_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}'
        self.engine_name = "ThreatCrowd"
        self.q = q
        super(ThreatCrowd, self).__init__(base_url, self.engine_name, domain, subdomains, q=q)
        return

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
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
                    self.subdomains.append(subdomain.strip())
        except Exception as e:
            pass