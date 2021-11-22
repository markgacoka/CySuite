from scripts.subdomains.apis.anubis import anubis_script
from scripts.subdomains.apis.findsubdomains import findsubdomains_script
from scripts.subdomains.apis.hackertarget import hackertarget_script
from scripts.subdomains.apis.openthreat import openthreat_script
from scripts.subdomains.apis.projectsonar import projectsonar_script
from scripts.subdomains.apis.projectsonar2 import projectsonar_script2
from scripts.subdomains.apis.riddler import riddler_script
from scripts.subdomains.apis.shodan import shodan_script
from scripts.subdomains.apis.threatcrowd import threatcrowd_script
from scripts.subdomains.apis.threatcrowd2 import ThreatCrowd
from scripts.subdomains.apis.virustotal import virustotal_script
from scripts.subdomains.apis.virustotal2 import Virustotal

# Archives
from scripts.subdomains.archives.commoncrawl import commoncrawl_script
from scripts.subdomains.archives.waybackmachine import waybackmachine_script

# Certificates
from scripts.subdomains.certificates.censys import censys_script
from scripts.subdomains.certificates.certspotter import certspotter_script
from scripts.subdomains.certificates.crt import crt_script
from scripts.subdomains.certificates.crt2 import CrtSearch
from scripts.subdomains.certificates.entrust_certificates import entrust_certificates_script
from scripts.subdomains.certificates.google_transparency import google_transparency_script

# DNS databases
from scripts.subdomains.dnsdatabases.dnsdb import dnsdb_script
from scripts.subdomains.dnsdatabases.dnstrails import dnstrails_script
from scripts.subdomains.dnsdatabases.passivedns import PassiveDNS
from scripts.subdomains.dnsdatabases.passivetotal import passivetotal_script

# Search Engines
from scripts.subdomains.search_engines.ask import AskEnum
from scripts.subdomains.search_engines.baidu import BaiduEnum
from scripts.subdomains.search_engines.bing import BingEnum
from scripts.subdomains.search_engines.dnsdumpster import DNSdumpster
from scripts.subdomains.search_engines.google import GoogleEnum
from scripts.subdomains.search_engines.netcraft import NetcraftEnum
from scripts.subdomains.search_engines.yahoo import YahooEnum
from scripts.subdomains.search_engines.threaders import main
import yarl

def cleanup(subdomain_lst):
    clean_lst = []
    for domain in subdomain_lst:
        if domain.strip() == '' or domain == None:
            pass
        if '\n' in domain:
            intermediary = domain.split('\n')
            for i in intermediary:
                clean_lst.append(i)
        else:
            clean_lst.append(domain)
    for idx, subdomain in enumerate(clean_lst):
        if subdomain.startswith('https://'):
            if yarl.URL(subdomain).path_qs != '' or  yarl.URL(subdomain).path_qs != '/':
                clean_lst[idx] = str(yarl.URL(subdomain).origin())[8:].strip()
        elif subdomain.startswith('http://'):
            if yarl.URL(subdomain).path_qs != '' or yarl.URL(subdomain).path_qs != '/':
                clean_lst[idx] = str(yarl.URL(subdomain).origin())[7:].strip()
        else:
            if subdomain.strip() != '' and subdomain != None:
                subdomain_full = 'http://' + str(subdomain)
                subdomain_yarl = yarl.URL(subdomain_full)
                if subdomain_yarl.path_qs != '' or subdomain_yarl.path_qs != '/':
                    clean_lst[idx] = str(subdomain_yarl.origin())[7:].strip()
    return list(filter(None, set(clean_lst)))

def subdomain_list(domain):
    final_subdomains = projectsonar_script(domain)
    final_subdomains = cleanup(final_subdomains)
    yield final_subdomains