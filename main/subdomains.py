import sys
import yarl
import multiprocessing

# APIs
sys.path.insert(1, 'scripts/Subdomains/apis')
from anubis import anubis_script
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
from crt2 import CrtSearch
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
from bing import BingEnum
from dnsdumpster import DNSdumpster
from google import GoogleEnum
from netcraft import NetcraftEnum
from yahoo import YahooEnum
from threaders import main

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
                clean_subdomains[idx] = str(yarl.URL(subdomain_yarl_result))[7:]
        else:
            subdomain_yarl_result = subdomain_yarl
            if yarl.URL(subdomain_yarl_result).path_qs != '' and yarl.URL(subdomain_yarl_result).path_qs != '/':
                if 'https' in str(subdomain_yarl_result):
                    clean_subdomains[idx] = str(yarl.URL(subdomain_yarl_result.origin()))[8:]
                else:
                    clean_subdomains[idx] = str(yarl.URL(subdomain_yarl_result.origin()))[7:]
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

    final_subdomains += waybackmachine_script(domain)

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