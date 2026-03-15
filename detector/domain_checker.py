import whois
from datetime import datetime


def check_domain_repuation(domain):
    pass

def check_domain_age(domain):

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