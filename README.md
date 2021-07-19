<h1 align="center">
  <img src="assets/img/icons/cysuite.png" alt="CySuite logo" width="200px"></a>
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" />
  <img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" />
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
</p>

# CySuite
CySuite is a web-security automation tool designed to ease recon and vulnerability assessment in web targets. This tool is suited for bug bounty hunters, penetration testers and cybersecurity enthusiasts with interest in security automation. 

CySuite is designed to scan and test for all classic vulnerabilities in the OWASP Top 10 list. It starts with passive and active reconnaissance, stores the result to a database, then scans for attack vectors in which a potential vulnerability might lie. It also offers a myriad of tools for vulnerability assessment such as request manipulators, wordlist generators, code injectors and various encoders/decoders.

Please make sure to read the [CONTRIBUTING](CONTRIBUTING.md) and [CODE OF CONDUCT](CODE_OF_CONDUCT.md) pages before joining the community or contributing.

## Features
### Subdomain Enumeration
The subdomain enumeration section of Cysuite scans for subdomains both passively and actively.

#### Bruteforce 
A dataset/wordlist of your choice can be provided to bruteforce possible subdomains.
    - The number of threads and requests/second can be changed.
    - The results are saved to the local database for future reference, future intergration and efficient rescans.
    - Comes with all.txt, commonspeak2 and Seclist's subdomains-top1million-110000.txt wordlists built-in.

#### Passive Scan
Passive archives such as Rapid7 FDNS dataset can be queried for additional subdomains (online version only)

**Output**: 
subdomains, related IP addresses (IPv4), status codes, Web Application Firewall (WAF), Server Type, homepage screenshot (if possible).

# Methods
1. Subdomain bruteforcing
	- ffuf, gobuster, knock, dnssearch, sudomy, subbrute
2. DNS walking
	- ldns-walk, amass
4. DNS Zone Transfer
	- dnscan, DNSRecon, dig, amass
5. Certificate Transparency Logs
	- censys.io, scans.io (Censys and Project Sonar), cert.sh, san_subdomain_enum.py

6. Subdomain archive datasets and APIs
	- Rapid7 Project Sonar or https://sonar.omnisint.io/subdomains/google.com [Dataset]
	- Common Crawl or CCrawlDNS.py [API]
	- Shodan [API]
	- AnubisDB or https://jldc.me/anubis/subdomains/sony.com [API]
	- Chaos [API]
	- Recon.dev [API]
	- SecurityTrails or haktrails [API]
	- bufferover or https://dns.bufferover.run/dns?q=.sony.com FDNS [API]
	- Crt.sh or https://crt.sh/?q=markgacoka.com
	- VirusTotal - 'https://www.virustotal.com/vtapi/v2/url/scan'
	- Censys -  subdomain_enum_censys.py 
	- VirusTotal API - virustotal_subdomain_enum.py

7. Search Engine Dorking
	- Google, Yahoo, Bing, Baidu, Ask
	- Knock
8, Reverse DNS lookups on identified public IPs
	- Lepus, amass
9. Search subdomains in JS files
	- jsubfinder
11. Search subdomains using github
	- github-subdomains.py
12, DNS subdomain permutation
	- altdns, amass
13. DNS record information
	- https://bgp.he.net/dns/google.com
14, Subdomains from passive sources:
	- dnsdumpster.py
15. NSEC3 hash cracking
	- nsec3walker, nsec3map
16. Using cloudflare service
	- cloudflare_enum.py
17. Resolving active subdomains
	- MassDNS

