from django import forms

from .models import CustomUser, Profile, Role, GENDERS, BIRTH_SEX
from monitoria.models import Category


class UserProfileForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )

    name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[("", "Selecione")] + GENDERS,
        widget=forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    birth_sex = forms.ChoiceField(
        required=False,
        choices=[("", "Selecione")] + BIRTH_SEX,
        widget=forms.Select(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    code_nr = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )
    code_senior = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"}),
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["username"].initial = self.instance.username
            self.fields["email"].initial = self.instance.email
            self.fields["roles"].initial = self.instance.roles.all()
            profile = getattr(self.instance, "profile", None)
            if profile:
                self.fields["name"].initial = profile.name
                self.fields["category"].initial = profile.category
                self.fields["gender"].initial = profile.gender
                self.fields["birth_sex"].initial = profile.birth_sex
                self.fields["code_nr"].initial = profile.code_nr
                self.fields["code_senior"].initial = profile.code_senior
        else:
            self.fields["password"].required = True

    def save(self):
        user = self.instance or CustomUser()
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.save()
        user.roles.set(self.cleaned_data["roles"])
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        elif not self.instance:
            user.set_unusable_password()
            user.save()

        profile = getattr(user, "profile", None)
        if not profile:
            profile = Profile(user=user)
        profile.name = self.cleaned_data["name"]
        profile.category = self.cleaned_data["category"]
        profile.gender = self.cleaned_data["gender"]
        profile.birth_sex = self.cleaned_data["birth_sex"]
        profile.code_nr = self.cleaned_data["code_nr"]
        profile.code_senior = self.cleaned_data["code_senior"]
        profile.save()
        return user
