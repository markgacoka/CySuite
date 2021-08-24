<h1 align="center">
  <img src="templates/static/img/icons/cysuite.png" alt="CySuite logo" width="200px"></a>
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

VALUES: Lean, Fast, Organized

## Features
### Subdomain Enumeration
The subdomain enumeration section of Cysuite scans for subdomains both passively and actively.

#### Bruteforce 
A dataset/wordlist of your choice can be provided to bruteforce possible subdomains.
    - The number of threads and requests/second can be changed.
    - The results are saved to the local database for future reference, future intergration and efficient rescans.
    - Comes with all.txt, commonspeak2 and Seclist's subdomains-top1million-110000.txt wordlists built-in.

**Passive archives**
- Rapid7 FDNS dataset
- The Wayback Machine
- CommonCrawl

**Search engines**
- Google
- Bing
- Ask
- Baidu
- Netcraft
- Yahoo
- DNSDumpster

**Certificate Authorities** 
- Certspotter
- Google transparency logs
- Entrust certificates
- Crt.sh

**DNS infrastructure**
- DNSDB
- DNSTrails
- PassiveDNS

**Threat detection APIs**
- OpenThreat
- PassiveTotal
- VirusTotal
- Threatcrowd
- Censys
- Shodan
- F-Secure Riddler
- HackerTarget

**Output**: 
subdomains, related IP addresses (IPv4), status codes, Web Application Firewall (WAF), Server Type, homepage screenshot (if possible).

For more information on the database models used, check the [API Docs page](scripts/API.md)

### Run the program
```
git clone https://github.com/markgacoka/CySuite
cd CySuite
pipenv install
pipenv shell
pipenv install -r requirements.txt

# Asynchronicity (Redis, Celery and RabbitMQ)
docker run -d -p 5672:5672 rabbitmq 
docker run -d -p 6379:6379 redis
redis-server
celery -A cysuite worker -l info

# Creating a superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Remove all pycache files
```
find . -type d -name __pycache__ -exec rm -r {} \+
```

### Before launch
{https://www.youtube.com/watch?v=mAeK4Ia4fk8}
[ ] Hide secret key in `secret.txt` or `.env`
[ ] Install SSL certificate in Django
  - HSTS settings
  - Add SESSION_COOKIE, CSRF and SECURE_SSL settings
[ ] Flush database and make migrations afresh
[ ] Allowed Hosts (add the real domain name)
[ ] Copy static files to root directory
  - `python manage.py collectstatic`
[ ] Change settings.py from `DEBUG=True` to `DEBUG=FALSE`
[ ] `python manage.py check --deploy`
[ ] Change admin URL