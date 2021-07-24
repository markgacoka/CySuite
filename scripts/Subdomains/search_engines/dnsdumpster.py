

import threading
import requests
from .searchparser import Parser
from .searchutils import Core

class DNSdumpster(EnumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        
        self.live_subdomains = []
        self.engine_name = "DNSdumpster"
        self.threads = 70
                
        self.domain = domain.replace(' ', '%20')
        
        self.results = ""
        self.totalresults = ""
        self.server = 'dnsdumpster.com'
        self.base_url = self.server

        self.lock = threading.BoundedSemaphore(value=self.threads)
        self.q = q
        super(DNSdumpster, self).__init__(self.base_url, self.engine_name, domain, subdomains, q=q)
        
        self.targetdomain = domain
        
        return

    def do_search(self):
        try:
            agent = Core.get_user_agent()
            headers = {'User-Agent': agent}
            session = requests.session()
            # create a session to properly verify
            url = f'https://{self.server}'
            request = session.get(url, headers=headers)
            cookies = str(request.cookies)
            # extract csrftoken from cookies
            csrftoken = ''
            for ch in cookies.split("=")[1]:
                if ch == ' ':
                    break
                csrftoken += ch
            data = {
                'Cookie': f'csfrtoken={csrftoken}', 'csrfmiddlewaretoken': csrftoken, 'targetip': self.targetdomain}
            headers['Referer'] = url
            post_req = session.post(url, headers=headers, data=data)
            self.results = post_req.text
            
        except Exception as e:
            print(f'An exception occured: {e}')
        self.totalresults += self.results

    def extract_domains(self):
        rawres = Parser(self.totalresults, self.targetdomain)  
        self.live_subdomains =  rawres.hostnames()
        for sub in self.live_subdomains:
            self.subdomains.append(sub)
        
    def enumerate(self):
        self.do_search()  # Only need to do it once.
        self.extract_domains() 
        return self.subdomains 
        
    def get_people(self):
        return []
    
    def get_ipaddresses(self):
        return [] 