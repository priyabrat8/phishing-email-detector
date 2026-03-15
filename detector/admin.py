from django.contrib import admin
from .models import ScanResult
# Register your models here.

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['email_text', 'result', 'risk_score', 'created_at',]
    list_filter = ['risk_score', 'created_at', 'result']
    search_fields = ['email_text']