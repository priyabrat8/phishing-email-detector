from django.db import models

# Create your models here.

class ScanResult(models.Model):
    email_text = models.TextField()
    email_sender = models.EmailField()
    result = models.CharField(max_length=50)
    risk_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)