from django import forms

from .models import Payment, Rating


class PaymentStatusForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            )
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["profile", "event", "score", "description"]
        widgets = {
            "profile": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "event": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "score": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
        }
