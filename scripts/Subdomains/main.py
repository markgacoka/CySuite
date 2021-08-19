from apis.anubis import anubis_script
from apis.findsubdomains import findsubdomains_script
from apis.hackertarget import hackertarget_script
from apis.openthreat import openthreat_script
from apis.projectsonar import projectsonar_script
from apis.projectsonar2 import projectsonar_script2
from apis.riddler import riddler_script
from apis.shodan import shodan_script
from apis.threatcrowd import threatcrowd_script
from apis.virustotal import virustotal_script
from apis.virustotal2 import Virustotal

from archives.commoncrawl import commoncrawl_script
from archives.waybackmachine import waybackmachine_script

from certificates.censys import censys_script
from certificates.certspotter import certspotter_script
from certificates.crt import crt_script
from certificates.entrust_certificates import entrust_certificates_script
from certificates.google_transparency import google_transparency_script

from dnsdatabases.dnsdb import dnsdb_script
from dnsdatabases.dnstrails import dnstrails_script
from dnsdatabases.passivedns import PassiveDNS
from dnsdatabases.passivetotal import passivetotal_script

from search_engines.ask import AskEnum
from search_engines.baidu import BaiduEnum
from search_engines.dnsdumpster import DNSdumpster
from search_engines.netcraft import NetcraftEnum
from search_engines.yahoo import YahooEnum

url = "google.com"
# works needs_api

# APIs
# print(anubis_script(url)) # y n
# print(findsubdomains_script(url)) # n n
# print(hackertarget_script(url)) # y n
# print(openthreat_script(url)) # y n
# print(projectsonar_script(url)) # y n
# print(projectsonar_script2(url)) # y n
# print(riddler_script(url)) # n y [free]
# print(shodan_script(url)) # y y [free]
# print(threatcrowd_script(url)) # y n
# print(virustotal_script(url)) # y y [free]

# vt = Virustotal(url)
# vt.enumerate()
# print(vt.subdomains) # y y [paid]

# Archives y n
# print(commoncrawl_script(url)) # n n
# print(waybackmachine_script(url)) # y n

# Certificates
# print(censys_script(url)) # n y [Free]
# print(certspotter_script(url)) # n n
# print(crt_script(url)) # y n
# print(entrust_certificates_script(url)) y n [blocked]
# print(google_transparency_script(url)) y n [blocked]

# DNS Databases
# print(dnsdb_script(url)) # n n
# print(dnstrails_script(url)) # y y [free]

# pdns = PassiveDNS(url)
# pdns.enumerate()
# print(pdns.subdomains) # y n

print(passivetotal_script(url)) # y y [free] [test-again Retry-After]

# Search Engines - All don't work at the moment
# ask = AskEnum(url)
# ask.enumerate()
# print(ask.subdomains)

# baidu = BaiduEnum(url)
# baidu.enumerate()
# print(baidu.subdomains)

# bing = BingEnum(url)
# bing.enumerate()
# print(bing.subdomains)

# dnsdumpster = DNSdumpster(url)
# dnsdumpster.enumerate()
# print(dnsdumpster.subdomains)

# netcraft = NetcraftEnum(url)
# netcraft.enumerate()
# print(netcraft.subdomains)

# yahoo = YahooEnum(url)
# yahoo.enumerate()
# print(yahoo.subdomains)



