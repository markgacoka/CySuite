import whois

def is_registered(domain_name):
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)


def whois_info(domain_name):
    if is_registered(domain_name):
        whois_info = whois.whois(domain_name)
        return whois_info   

domain = 'markgacoka.com'
print("Registered: ", is_registered(domain))
print(whois_info(domain))

