from django.contrib import admin
from .models import ScanResult, PhishingURL
# Register your models here.

admin.site.register(ScanResult)

@admin.register(PhishingURL)
class PhishingURLAdmin(admin.ModelAdmin):
    list_display = ['domain', 'source', ]
    list_filter = ['source']
    search_fields = ['domain']