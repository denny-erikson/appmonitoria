from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Cancellation

@receiver(post_save, sender=Cancellation)
def cancelar_disponibilidade(sender, instance, created, **kwargs):
    """Cancela a disponibilidade associada quando um novo Cancellation é criado."""
    if created and instance.availability:
        availability = instance.availability
        availability.status = False
        availability.summoned = False
        availability.cancellation = instance
        availability.save()
