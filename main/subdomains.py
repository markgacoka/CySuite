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
    new_lst = []
    for subdomain in subdomain_lst:
        if '\n' in subdomain:
            intermediary = subdomain.split('\n')
            for i in intermediary:
                new_lst.append(i)
        else:
            new_lst.append(subdomain)
    clean_subdomains = list(set(new_lst))

    for idx, subdomain in enumerate(clean_subdomains):
        subdomain_yarl = yarl.URL(subdomain)
        if not subdomain_yarl.is_absolute():
            subdomain_yarl_result = 'http://' + str(subdomain_yarl)
            if yarl.URL(subdomain_yarl_result).path_qs != '' and yarl.URL(subdomain_yarl_result).path_qs != '/':
                clean_subdomains[idx] = str(yarl.URL(subdomain_yarl_result))[7:].strip()
        else:
            subdomain_yarl_result = subdomain_yarl
            if yarl.URL(subdomain_yarl_result).path_qs != '' and yarl.URL(subdomain_yarl_result).path_qs != '/':
                if 'https' in str(subdomain_yarl_result):
                    clean_subdomains[idx] = str(yarl.URL(subdomain_yarl_result.origin()))[8:].strip()
                else:
                    clean_subdomains[idx] = str(yarl.URL(subdomain_yarl_result.origin()))[7:].strip()
    return list(set(clean_subdomains))

def subdomain_list(domain):
    final_subdomains = []

    # APIs
    final_subdomains += anubis_script(domain)
    final_subdomains += findsubdomains_script(domain)
    final_subdomains += hackertarget_script(domain)
    final_subdomains += openthreat_script(domain)
    final_subdomains += projectsonar_script(domain)
    final_subdomains += projectsonar_script2(domain)
    final_subdomains += threatcrowd_script(domain)
    # Archives
    final_subdomains += waybackmachine_script(domain)
    # Certificated
    final_subdomains += certspotter_script(domain)
    final_subdomains += crt_script(domain)
    # GoogleEnum and VirusTotal removed
    chosenEnums = [CrtSearch, ThreatCrowd, BaiduEnum, YahooEnum, BingEnum, AskEnum, NetcraftEnum, DNSdumpster, PassiveDNS]
    threaders = main(domain, chosenEnums)
    final_subdomains += threaders

    print("Cleaning up...")
    final_subdomains = cleanup(final_subdomains)
        
    # Needs token
    # final_subdomains += shodan_script(domain)
    # final_subdomains += riddler_script(domain)
    # final_subdomains += virustotal_script(domain)
    # final_subdomains += censys_script(domain)
    # final_subdomains += dnstrails_script(domain)

    # TO-DO
    # final_subdomains += commoncrawl_script(domain)
    # final_subdomains += entrust_certificates_script(domain)
    # final_subdomains += google_transparency_script(domain)
    # final_subdomains += dnsdb_script(domain)
    
    # Also needs token
    # final_subdomains += passivetotal_script(domain)
    yield final_subdomains