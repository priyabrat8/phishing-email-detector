import re
from urllib.parse import urlparse
from .domain_checker import check_domain_age, check_domain_reputation

def normalize_obfuscation(text):
    replacements = {
        "hxxp://": "http://",
        "hxxps://": "https://",
        "[.]": ".",
        "(.)": ".",
        " dot ": "."
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

def extract_urls(text):
    text = normalize_obfuscation(text)
    url_pattern = re.compile(
        r'\b((?:https?|ftp)://[A-Za-z0-9\-._~:/?#@!$&\'()*+,;=%]+)',
        re.IGNORECASE
    )

    matches = url_pattern.findall(text)

    return matches

def url_checker(text):
    score = 0
    reasons = []
    urls = []
    matches = extract_urls(text)

    for url in matches:
        url = url.rstrip('.,!?:;)"\'')
        parsed = urlparse(url)

        # ensure valid domain or IP exists
        if parsed.scheme and parsed.netloc:
            urls.append(url)
        else:
            reasons.append(f"URL: {url} is malformed.")
            score += 10
            break
        
        if parsed.scheme == 'http':
            score += 15
            reasons.append(f"URL: {url} uses HTTP instead of HTTPS.") 
        
        domain = parsed.netloc.lower()
        domain = domain.split(':')[0]

        # url domain age checker
        is_suspicious_domain, domain_age = check_domain_age(domain)
        if is_suspicious_domain:
            score += 15
            reasons.append(f"URL domain: {domain} is very new ({domain_age} days old).")
        
        # check IP
        if re.match(r'\d+\.\d+\.\d+\.\d+', domain):
            score += 20
            reasons.append("IP address used")

        # hyphen phishing domain
        if "-" in domain:
            score += 5
            reasons.append("Hyphenated domain")

        # very long domain
        if len(domain) > 30:
            score += 5
            reasons.append("Very long domain")
        
        # check for domain in known phishing database
        if check_domain_reputation(domain):
            score += 25
            reasons.append(f"\"{domain}\" is found in phishing database.")


    return {'urls': list(set(urls)), 'reasons': reasons, 'score': score}