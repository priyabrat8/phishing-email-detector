import whois
from datetime import datetime
from .models import PhishingURL
from urllib.parse import urlparse


def check_domain_reputation(domain):
    if "://" in domain:
        domain = urlparse(domain).netloc.lower()
    else:
        domain = domain.lower()

    # Remove port
    domain = domain.split(':')[0]
    parts = domain.split('.')
    
    for i in range(len(parts) - 1):
        test_domain = ".".join(parts[i:])
        
        if PhishingURL.objects.filter(domain=test_domain).exists():
            return True # 

    return False 

def check_domain_age(domain):
    # format -> Only domain , no path and port
    try:
        domain_info = whois.whois(domain)

        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        age_days = (datetime.now() - creation_date).days

        if age_days < 30:
            return True, age_days

        return False, age_days

    except:
        return False, None