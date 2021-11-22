from os.path import join
from dns.resolver import Resolver, NXDOMAIN, NoAnswer, NoNameservers, Timeout

def getDNSrecords(domain):
    RES = {}
    MX = []
    NS = []
    A = []
    AAAA = []
    SOA = []
    TXT = []

    resolver = Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1

    rrtypes = ["A", "MX", "NS", "AAAA", "SOA", "TXT"]

    for r in rrtypes:
        try:
            Aanswer = resolver.resolve(domain, r)
            for answer in Aanswer:
                if r == "A":
                    A.append(answer.address)
                    RES.update({r: A})
                if r == "MX":
                    MX.append(answer.exchange.to_text()[:-1])
                    RES.update({r: MX})
                if r == "NS":
                    NS.append(answer.target.to_text()[:-1])
                    RES.update({r: NS})
                if r == "AAAA":
                    AAAA.append(answer.address)
                    RES.update({r: AAAA})
                if r == "SOA":
                    SOA.append(answer.mname.to_text()[:-1])
                    RES.update({r: SOA})
                if r == "TXT":
                    TXT.append(str(answer))
                    RES.update({r: TXT})
        except (NXDOMAIN, NoAnswer, EmptyLabel, NoNameservers, DNSException, Timeout):
            pass
    return RES

print(getDNSrecords('markgacoka.com'))