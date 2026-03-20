from django.shortcuts import render
from .forms import EmailPostForm
from .models import ScanResult
from .ai_model import predict_email
from .url_checker import url_checker
from .sender_validation import sender_validation
from phishing_detector import settings
from django_ratelimit.decorators import ratelimit
import requests

# Create your views here.
def home(request):
    safe, created_safe = ScanResult.objects.get_or_create(status="safe")
    phishing, created_phishing = ScanResult.objects.get_or_create(status="phishing")
    safe_count , phishing_count = safe.count, phishing.count
    total_scans = safe_count + phishing_count
    
    if total_scans > 0:
        unsafe_percentage = int((phishing_count / total_scans) * 100)
        safe_percentage = 100 - unsafe_percentage
    else:
        safe_percentage = 100
        unsafe_percentage = 0
        total_scans = 0
    
    return render(request, 'pages/home.html', {
        "safe_count": safe_count,
        "unsafe_count": phishing_count,
        "total_scans": total_scans,
        "safe_percentage": safe_percentage,
        "unsafe_percentage": unsafe_percentage

    })

def contact(request):
    return render(request, 'pages/contact.html')

def terms(request):
    return render(request, 'pages/terms.html')

@ratelimit(key='ip', rate='4/m', block=True)
def scan_email(request):
    result = None
    score = 0
    message = None
    reasons = []
    form = EmailPostForm()
    safe, _ = ScanResult.objects.get_or_create(status="safe")
    phishing, _ = ScanResult.objects.get_or_create(status="phishing")

    if request.method == "POST":
        if request.POST.get('bot_catcher'):
            message = "Invalid request."
        else:
            # --- CLOUDFLARE TURNSTILE CHECK ---
            turnstile_token = request.POST.get('cf-turnstile-response')
            
            # Ask Cloudflare if the token is valid
            cf_request = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': settings.TURNSTILE_SECRET_KEY,
                    'response': turnstile_token
                }
            )
            cf_result = cf_request.json()
            form = EmailPostForm(request.POST)    

            # validate input
            if form.is_valid():
                try:
                    cd = form.cleaned_data
                    email_text = cd['email_text'].strip()
                    email_sender = cd['email_sender'].strip()
                    prediction, prob = predict_email(email_text)

                    score += round(prob * 100, 2)

                    if prediction == 1:
                        reasons.append("Phishing language detected")
                        result = "Phishing"
                    else:                    
                        result = "Safe"

                    # domain checker for sender's email
                    sender_score, sender_reasons = sender_validation(email_sender)
                    if sender_score >0 and sender_reasons:
                        score += sender_score
                        reasons.extend(sender_reasons)

                    # email body url domain checker
                    urls = url_checker(email_text)
                    if isinstance(urls, dict) and 'score' in urls:
                        score += urls['score']
                        reasons.extend(urls.get('reasons', []))
                    
                    if score > 100:
                        score = 100
                    
                    if score >= 60 and result != "Phishing":
                        result = "Suspicious"
                        reasons.append("Overall risk score is high.")

                    # save scan history
                    if result == "Safe":    
                        safe.count += 1
                        safe.save()
                    else:
                        phishing.count += 1
                        phishing.save()

                except Exception as e:
                    message = "Error in analyzing email."
            else:
                message = "Please enter a valid email address and message."
            
    return render(
        request,
        "pages/scan.html",
        {
            "form": form,
            "result": result,
            "score": score,
            "message": message,
            "reasons": reasons,
            "turnstile_site_key" : settings.TURNSTILE_SITE_KEY
        }
    )