from django.db import models
from events.models import Event
from users.models import CustomUser, Profile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Location(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    reimbursement_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        location = f"{self.city}, " if self.city else ""
        location += f"{self.state}, " if self.state else ""
        location += self.country
        return f"Região: {location} - Reembolso: R$ {self.reimbursement_value:.2f}"


class Address(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)

    def __str__(self):
        return self.address

class BankAccount(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_agency = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    key_pix = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.bank_name


WORK_REGIME = [
    ('regime_clt', 'Regime CLT'),
    ('regime_pj', 'Regime PJ'),
]

class Document(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rg_number = models.CharField(max_length=10, null=True, blank=True)
    cpf_number = models.CharField(max_length=11, null=True, blank=True)
    pis_number = models.CharField(max_length=20, null=True, blank=True)
    cnpj_number = models.CharField(max_length=14, null=True, blank=True)
    municipal_registration = models.CharField(max_length=50, null=True, blank=True)
    work_regime = models.CharField(choices=WORK_REGIME, default='regime_clt', max_length=10)

    def __str__(self):
        return self.Documents_type
    

SIZE_CHOICES = [
    ('P', 'Pequeno'),
    ('M', 'Médio'),
    ('G', 'Grande'),
    ('GG', 'Extra Grande'),
]

class Uniform(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    t_shirt_size = models.CharField(max_length=2, blank=True, null=True, help_text="Select t-shirt size", choices=SIZE_CHOICES)
    pants_size = models.CharField(max_length=2, blank=True, null=True, help_text="Select pants size", choices=SIZE_CHOICES)
    shorts_size = models.CharField(max_length=2, blank=True, null=True, help_text="Select shorts size", choices=SIZE_CHOICES)
    jacket_size = models.CharField(max_length=2, blank=True, null=True, help_text="Select jacket size", choices=SIZE_CHOICES)
    festival_shirt_size = models.CharField(max_length=2, blank=True, null=True, help_text="Select festival shirt size", choices=SIZE_CHOICES)
    party_uniform_size = models.CharField(max_length=2, blank=True, null=True, help_text="Select party uniform size", choices=SIZE_CHOICES)

    def __str__(self):
        return f"Uniforms for {self.user.username}"



class Payment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __decimal__(self):
        return self.amount
