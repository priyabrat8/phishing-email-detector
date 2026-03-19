import uuid
from django.db import models

# Create your models here.

class ScanResult(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    status = models.CharField(max_length=20, unique=True, default="safe")
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Scan Statistics"

class PhishingURL(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    domain = models.CharField(max_length=255, db_index=True, unique=True)
    source = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain
    
    class Meta:
        indexes = [
            models.Index(fields=['domain']),
        ]