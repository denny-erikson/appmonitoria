from django import forms
from .models import Event, Team, Availability, Cancellation, Product, Resort

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


class AvailabilityCreateForm(forms.ModelForm):
    cancel_reason = forms.CharField(
        required=False,
        label="Motivo do cancelamento",
        widget=forms.TextInput(
            attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}
        ),
    )

    class Meta:
        model = Availability
        fields = ['profile', 'status', 'summoned']
        widgets = {
            'profile': forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            'status': forms.CheckboxInput(attrs={"class": "h-4 w-4 text-indigo-600"}),
            'summoned': forms.CheckboxInput(attrs={"class": "h-4 w-4 text-indigo-600"}),
        }

    def save_with_team(self, team):
        availability = self.save(commit=False)
        availability.team = team
        availability.save()
        reason = self.cleaned_data.get("cancel_reason")
        if reason:
            cancellation = Cancellation.objects.create(reason=reason, availability=availability)
            availability.cancellation = cancellation
            availability.status = False
            availability.save()
        return availability


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "events"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}
            ),
            "events": forms.SelectMultiple(
                attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}
            ),
        }


class ResortForm(forms.ModelForm):
    class Meta:
        model = Resort
        fields = ["name", "events"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}
            ),
            "events": forms.SelectMultiple(
                attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}
            ),
        }
