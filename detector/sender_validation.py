from .domain_checker import check_domain_age, check_domain_reputation

def sender_validation(email_sender):
    score = 0
    reasons = []
    try:
        is_suspicious_domain, domain_age = check_domain_age(email_sender.split('@')[1])

        if is_suspicious_domain:
            score += 15
            reasons.append(f"Sender's Domain very new ({domain_age} days old)")
    except:
        pass
    
    if check_domain_reputation(email_sender.split('@')[1]):
        score += 10
        reasons.append("Sender's email domain has a poor reputation")
    
    return score, reasons