from django.db import models
from users.models import  Profile
from django.core.exceptions import ValidationError

# Create your models here.
class Event(models.Model):
    produto = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    daily = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    event = models.OneToOneField('Event', on_delete=models.CASCADE, related_name="team", blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    max_availabilities = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.name} - {self.event}"

    def save(self, *args, **kwargs):
        # Primeiro salva o objeto para garantir que tenha uma chave primária
        super().save(*args, **kwargs)
        
        # Validação após o salvamento
        if self.availabilities.count() > self.max_availabilities:
            raise ValidationError(f"O time não pode ter mais de {self.max_availabilities} disponibilidades.")


class Availability(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="availabilities", blank=True, null=True)
    status = models.BooleanField(default=False)
    summoned = models.BooleanField(default=False)
    cancellation = models.ForeignKey('Cancellation', on_delete=models.SET_NULL, blank=True, null=True, related_name='availabilities')

    def cancel(self, reason):
        """Cancela a disponibilidade e registra o motivo, se ainda não foi cancelado."""
        if not self.cancellation:
            cancellation = Cancellation.objects.create(reason=reason, availability=self)
            self.cancellation = cancellation
            self.status = False
            self.summoned = False
            self.save()

    def __str__(self):
        return f"{self.profile.name} está {'disponível' if self.status else 'indisponível'}"

class Cancellation(models.Model):
    reason = models.CharField(max_length=255)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name='cancellations', blank=True, null=True)

    def __str__(self):
        return self.reason
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    events = models.ManyToManyField('Event', related_name="products")
    def __str__(self):
        return self.name


class Resort(models.Model):
    name = models.CharField(max_length=100)
    availability = models.OneToOneField("Availability", on_delete=models.CASCADE)
    def __str__(self):
        return self.name