
import multiprocessing
import urllib.parse as urlparse

def subdomain_sorting_key(hostname):
    parts = hostname.split('.')[::-1]
    if parts[-1] == 'www':
        return parts[:-1], 1
    return parts, 0

def main(domain, chosenEnums):
    search_list = set()
    subdomains_queue = multiprocessing.Manager().list()

    if not domain.startswith('http://') or not domain.startswith('https://'):
        domain = 'http://' + domain

    parsed_domain = urlparse.urlparse(domain)
    enums = [enum(domain, [], q=subdomains_queue) for enum in chosenEnums]
    for enum in enums:
        enum.start()
    for enum in enums:
        enum.join()

    subdomains = set(subdomains_queue)
    for subdomain in subdomains:
        search_list.add(subdomain)

    if subdomains:
        subdomains = sorted(subdomains, key=subdomain_sorting_key)
    return subdomains