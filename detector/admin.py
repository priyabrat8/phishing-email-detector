from django.contrib import admin
from .models import ScanResult, PhishingURL
# Register your models here.

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['email_text', 'result', 'risk_score', 'created_at',]
    list_filter = ['result']
    search_fields = ['email_text']

@admin.register(PhishingURL)
class PhishingURLAdmin(admin.ModelAdmin):
    list_display = ['domain', 'source', ]
    list_filter = ['source']
    search_fields = ['domain']