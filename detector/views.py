from django.shortcuts import render
from .domain_checker import check_domain_age
from .forms import EmailPostForm
from .models import ScanResult
from .ai_model import predict_email
from .url_checker import url_checker

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def scan_email(request):
    result = None
    score = 0
    message = None
    reasons = []
    form = EmailPostForm()

    if request.method == "POST":
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
                is_suspicious_domain, domain_age = check_domain_age(email_sender.split('@')[1])
                if is_suspicious_domain:
                    score += 15
                    reasons.append(f"Sender's Domain very new ({domain_age} days old)")
                
                # email body url domain checker
                urls = url_checker(email_text)

                score += urls['score']
                reasons.extend(urls['reasons'])
                
                if score > 100:
                    score = 100
                
                if score >= 60 and result != "Phishing":
                    result = "Suspicious"
                    reasons.append("Overall risk score is high.")

                # save scan history
                ScanResult.objects.create(
                    email_text=email_text,
                    email_sender=email_sender,
                    result=result,
                    risk_score=score
                )

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
            "reasons": reasons
        }
    )