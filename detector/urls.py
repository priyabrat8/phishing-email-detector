from django.urls import path
from . import views

app_name = 'detector'
urlpatterns = [
    path('', view=views.home, name='home'),
    path('scan/', view=views.scan_email, name='scan_email'),
]