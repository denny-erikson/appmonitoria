from django import forms

from .models import Category, Payment, Rating, Document, BankAccount, Uniform


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


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "user",
            "rg_number",
            "cpf_number",
            "pis_number",
            "cnpj_number",
            "municipal_registration",
            "work_regime",
        ]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "rg_number": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "cpf_number": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "pis_number": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "cnpj_number": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "municipal_registration": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "work_regime": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
        }


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["user", "bank_name", "account_agency", "account_number", "key_pix"]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "bank_name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "account_agency": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "account_number": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "key_pix": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
        }


class UniformForm(forms.ModelForm):
    class Meta:
        model = Uniform
        fields = [
            "user",
            "t_shirt_size",
            "pants_size",
            "shorts_size",
            "jacket_size",
            "festival_shirt_size",
            "party_uniform_size",
        ]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                }
            ),
            "t_shirt_size": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "pants_size": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "shorts_size": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "jacket_size": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "festival_shirt_size": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
            "party_uniform_size": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
        }
