from django import forms
from .models import Event, Team, Availability

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'daily', 'resort']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'status', 'max_availabilities']

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['profile', 'status', 'summoned']