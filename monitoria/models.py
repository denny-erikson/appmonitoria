from django.db import models
from users.models import CustomUser
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
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    def __str__(self):
        return self.bank_name

class Document(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    Documents_type = models.CharField(max_length=50)
    Documents_number = models.CharField(max_length=20)
    def __str__(self):
        return self.Documents_type

class Uniform(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    uniform_type = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    def __str__(self):
        return self.uniform_type

class Product(models.Model):
    name = models.CharField(max_length=50)
    events = models.ManyToManyField("Event", related_name="products")
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField("Team", related_name="events")
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)
    resort = models.OneToOneField("Resort", on_delete=models.CASCADE)
    payments = models.ManyToManyField("Payment", related_name="teams")

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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    def __decimal__(self):
        return self.amount
