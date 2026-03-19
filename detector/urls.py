from django.urls import path
from . import views

app_name = 'detector'
urlpatterns = [
    path('', view=views.home, name='home'),
    path('scan/', view=views.scan_email, name='scan_email'),
    path('contact/', view=views.contact, name='contact'),
    path('terms/', view=views.terms, name='terms'),
]