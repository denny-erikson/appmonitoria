from django.db import models
from users.models import Profile
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    """Representa um evento específico."""
    name = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    daily = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_active(self):
        """Verifica se o evento está ativo."""
        return self.start_date <= timezone.now().date() <= self.end_date

class Team(models.Model):
    """Representa um time associado a um evento."""
    event = models.OneToOneField('Event', on_delete=models.CASCADE, related_name="team", blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    max_availabilities = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.name} - {self.event}"

    def save(self, *args, **kwargs):
        # Primeiro, salve o objeto para garantir que ele tenha uma chave primária
        super().save(*args, **kwargs)
        
        # Validação após o salvamento inicial
        if self.availabilities.count() > self.max_availabilities:
            raise ValidationError(f"O time não pode ter mais de {self.max_availabilities} disponibilidades.")

    def get_members(self):
        """Obtém os membros do time."""
        return self.availabilities.filter(status=True)

class Availability(models.Model):
    """Representa a disponibilidade de um perfil para um time."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="availabilities", blank=True, null=True)
    status = models.BooleanField(default=False)
    summoned = models.BooleanField(default=False)
    cancellation = models.ForeignKey('Cancellation', on_delete=models.SET_NULL, blank=True, null=True, related_name='availabilities')

    def __str__(self):
        return f"{self.team.name} - {self.profile.name} está {'disponível' if self.status else 'indisponível'}"

    def save(self, *args, **kwargs):
        # Verificar se o time está encerrado antes de salvar
        if self.team.status:
            self.status = False
        super().save(*args, **kwargs)

class Cancellation(models.Model):
    """Representa um cancelamento de disponibilidade."""
    reason = models.CharField(max_length=255)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name='cancellations', blank=True, null=True)

    def __str__(self):
        return self.reason

class Product(models.Model):
    """Representa um produto que pode estar associado a vários eventos."""
    name = models.CharField(max_length=50)
    events = models.ManyToManyField('Event', related_name="products")

    def __str__(self):
        return self.name

class Resort(models.Model):
    """Representa um resort que pode estar associado a vários eventos."""
    name = models.CharField(max_length=100)
    events = models.ManyToManyField('Event', related_name="resorts", blank=True)

    def __str__(self):
        return self.name