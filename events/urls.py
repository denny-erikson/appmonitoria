from django.urls import path
from .views import EventWizard

urlpatterns = [
    path('event_wizard/', EventWizard.as_view(), name='event_wizard'),
]