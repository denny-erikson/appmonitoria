from django.db import models
from users.models import CustomUser, Profile
from django.core.validators import MinValueValidator, MaxValueValidator


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

class Product(models.Model):
    name = models.CharField(max_length=50)
    events = models.ManyToManyField("Event", related_name="products")
    def __str__(self):
        return self.name

class Event(models.Model):
    produto = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50,  blank=True, null=True)
    start_date = models.DateField(auto_now_add=False,  blank=True, null=True)
    end_date = models.DateField(auto_now_add=False,  blank=True, null=True)
    daily = models.DecimalField(max_digits=2, decimal_places=2,  blank=True, null=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    event = models.OneToOneField("Event", on_delete=models.CASCADE, blank=True, null=True,)
    name = models.CharField(max_length=50, blank=True, null=True,)
    status = models.BooleanField(default=False, blank=True, null=True,)

class Resort(models.Model):
    name = models.CharField(max_length=100)
    availability = models.OneToOneField("Availability", on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Availability(models.Model):
    status = models.CharField(max_length=50)
    cancellation = models.OneToOneField("Cancellation", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.status

class Cancellation(models.Model):
    reason = models.CharField(max_length=255)
    def __str__(self):
        return self.reason

class Payment(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __decimal__(self):
        return self.amount
