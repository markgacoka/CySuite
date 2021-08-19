import threading, re
import hashlib
import urllib
from urllib.parse import urlparse
from .utils import EnumratorBaseThreaded

class NetcraftEnum(EnumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        self.base_url = 'https://searchdns.netcraft.com/?restriction=site+ends+with&host={domain}'
        self.engine_name = "Netcraft"
        self.lock = threading.Lock()
        super(NetcraftEnum, self).__init__(self.base_url, self.engine_name, domain, subdomains, q=q)
        self.q = q
        return

    def req(self, url, cookies=None):
        cookies = cookies or {}
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout, cookies=cookies)
        except Exception as e:
            print(e)
            resp = None
        return resp

    def get_next(self, resp):
        link_regx = re.compile('<A href="(.*?)"><b>Next page</b></a>')
        link = link_regx.findall(resp)
        link = re.sub('host=.*?%s' % self.domain, 'host=%s' % self.domain, link[0])
        url = 'http://searchdns.netcraft.com' + link
        return url

    def create_cookies(self, cookie):
        cookies = dict()
        cookies_list = cookie[0:cookie.find(';')].split("=")
        cookies[cookies_list[0]] = cookies_list[1]
        # hashlib.sha1 requires utf-8 encoded str
        cookies['netcraft_js_verification_response'] = hashlib.sha1(urllib.unquote(cookies_list[1]).encode('utf-8')).hexdigest()
        return cookies

    def get_cookies(self, headers):
        if 'set-cookie' in headers:
            cookies = self.create_cookies(headers['set-cookie'])
        else:
            cookies = {}
        return cookies

    def enumerate(self):
        start_url = self.base_url.format(domain='example.com')
        resp = self.req(start_url)
        if(resp):
            cookies = self.get_cookies(resp.headers)
            url = self.base_url.format(domain=self.domain)
            while True:
                resp = self.get_response(self.req(url, cookies))
                self.extract_domains(resp)
                if(isinstance(resp, int)):
                    break
                if 'Next page' not in resp:
                    return self.subdomains
                    break
                url = self.get_next(resp)

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                subdomain = urlparse.urlparse(link).netloc
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    print("{0} : {1}".format(self.engine_name, subdomain))
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list