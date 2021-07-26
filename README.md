<h1 align="center">
  <img src="cysuite/static/img/icons/cysuite.png" alt="CySuite logo" width="200px"></a>
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

For more information on the database models used, check the [API Docs page](scripts/API.md)

