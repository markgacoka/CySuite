import sys
import yarl

# APIs
sys.path.insert(1, 'scripts/Subdomains/apis')
from .anubis import anubis_script
from findsubdomains import findsubdomains_script
from hackertarget import hackertarget_script
from openthreat import openthreat_script
from projectsonar import projectsonar_script
from projectsonar2 import projectsonar_script2
from riddler import riddler_script
from shodan import shodan_script
from threatcrowd import threatcrowd_script
from threatcrowd2 import ThreatCrowd
from virustotal import virustotal_script
from virustotal2 import Virustotal

# Archives
sys.path.insert(1, 'scripts/Subdomains/archives')
from commoncrawl import commoncrawl_script
from waybackmachine import waybackmachine_script

# Certificates
sys.path.insert(1, 'scripts/Subdomains/certificates')
from censys import censys_script
from certspotter import certspotter_script
from crt import crt_script
from entrust_certificates import entrust_certificates_script
from google_transparency import google_transparency_script

# DNS databases
sys.path.insert(1, 'scripts/Subdomains/dnsdatabases')
from dnsdb import dnsdb_script
from dnstrails import dnstrails_script
from passivedns import PassiveDNS
from passivetotal import passivetotal_script

# Search Engines
sys.path.insert(1, 'scripts/Subdomains/search_engines')
from ask import AskEnum
from baidu import BaiduEnum
from dnsdumpster import DNSdumpster
from netcraft import NetcraftEnum
from yahoo import YahooEnum

def cleanup(subdomain_lst):
    for idx, subdomain in enumerate(subdomain_lst):
        subdomain_yarl = yarl.URL(subdomain)
        if not subdomain_yarl.is_absolute():
            subdomain_yarl_result = 'http://' + str(subdomain_yarl)
            if yarl.URL(subdomain_yarl_result).path_qs != '' and yarl.URL(subdomain_yarl_result).path_qs != '/':
                subdomain_lst[idx] = str(yarl.URL(subdomain_yarl_result))[7:]
        else:
            subdomain_yarl_result = subdomain_yarl
            if yarl.URL(subdomain_yarl_result).path_qs != '' and yarl.URL(subdomain_yarl_result).path_qs != '/':
                if 'https' in str(subdomain_yarl_result):
                    subdomain_lst[idx] = str(yarl.URL(subdomain_yarl_result.origin()))[8:]
                else:
                    subdomain_lst[idx] = str(yarl.URL(subdomain_yarl_result.origin()))[7:]
    return list(set(subdomain_lst))

def subdomain_list(domain):
    final_subdomains = []

    # APIs
    # final_subdomains += anubis_script(domain)
    # final_subdomains += findsubdomains_script(domain)
    # final_subdomains += hackertarget_script(domain)
    # final_subdomains += openthreat_script(domain)
    # final_subdomains += projectsonar_script(domain)
    # final_subdomains += projectsonar_script2(domain)
    # final_subdomains += threatcrowd_script(domain)
    # Needs token
    # final_subdomains += shodan_script(domain)
    # final_subdomains += riddler_script(domain)
    # final_subdomains += virustotal_script(domain)

    # Archives
    # final_subdomains += waybackmachine_script(domain)
    # Does not work
    # final_subdomains += commoncrawl_script(domain)

    # Certificates
    # final_subdomains += certspotter_script(domain)
    # final_subdomains += crt_script(domain)
    # Needs token
    # final_subdomains += censys_script(domain)
    # Does not work
    # final_subdomains += entrust_certificates_script(domain)
    # final_subdomains += google_transparency_script(domain)

    # DNS Databases
    # pdns = PassiveDNS(domain)
    # pdns.enumerate()
    # final_subdomains += pdns.subdomains
    # Needs token
    # final_subdomains += dnstrails_script(domain)
    # Does not work
    # final_subdomains += dnsdb_script(domain)
    # Both needs token and does not work
    # final_subdomains += passivetotal_script(domain)

    # Search engines
    # ask = AskEnum(domain)
    # ask.enumerate()
    # final_subdomains += ask.subdomains

    # baidu = BaiduEnum(domain)
    # baidu.enumerate()
    # final_subdomains += baidu.subdomains

    # bing = BingEnum(domain)
    # bing.enumerate()
    # final_subdomains += bing.subdomains

    # dnsdumpster = DNSdumpster(domain)
    # dnsdumpster.enumerate()
    # final_subdomains += dnsdumpster.subdomains

    # netcraft = NetcraftEnum(domain)
    # netcraft.enumerate()
    # final_subdomains += netcraft.subdomains

    # yahoo = YahooEnum(domain)
    # yahoo.enumerate()
    # final_subdomains += yahoo.subdomains

    # With threading - Search Engines
    if not domain.startswith('http://') or not domain.startswith('https://'):
        new_domain = 'http://' + domain
    else:
        new_domain = domain



    print("Cleaning up...")
    final_subdomains = cleanup(final_subdomains)

    yield final_subdomains
    
url = "coda.io"
print(next(subdomain_list(url)))