from django import forms

from .models import Category, Payment, Rating


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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title", "proficiency", "amount", "percentage"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "proficiency": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "percentage": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
        }
