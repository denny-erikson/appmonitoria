from django import forms

from .models import Payment


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
