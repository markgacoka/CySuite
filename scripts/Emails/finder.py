from emailfinder.extractor import *

def get_leaked_emails(domain):
    emails1 = get_emails_from_google(domain)
    emails2 = get_emails_from_bing(domain)
    emails3 = get_emails_from_baidu(domain)
    return emails1 + emails2 + emails3