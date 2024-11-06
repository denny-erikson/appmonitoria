from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging

from events.models import Availability, Cancellation
from monitoria.models import Category, Payment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Cancellation)
def cancel_availability(sender, instance, created, **kwargs):
    if created and instance.availability:
        logger.info("[Signal-cancel-availability] Signal triggered for cancellation.")
        availability = instance.availability
        availability.status = False
        availability.summoned = False
        availability.cancellation = instance
        availability.save()

        try:
            payment = Payment.objects.get(
                profile=availability.profile,
                event=availability.team.event
            )
            payment.status = "CANCELED"
            payment.save()
        except Payment.DoesNotExist:
            logger.warning("No payment found for the specified profile, team, and event.")
        except Payment.MultipleObjectsReturned:
            logger.error("Multiple payments found for the specified profile, team, and event.")

@receiver(post_save, sender=Availability)
def calculate_payment(sender, instance, created, **kwargs):
    """Calcula e salva o pagamento para um perfil associado a uma disponibilidade."""
    if created and instance.status == True:
        try:
            logger.info("[Signal-calculate-payment] Signal triggered for payment.")
            category = Category.objects.get(profile=instance.profile)
            base_amount = category.amount
            percentage_multiplier = Decimal(category.percentage / 100)
            total_category_payment = base_amount + (base_amount * percentage_multiplier)

            daily_rate = instance.team.event.daily or Decimal(0)
            payment_amount = total_category_payment * daily_rate

            Payment.objects.create(
                event=instance.team.event,
                profile=instance.profile,
                amount=payment_amount
            )

        except Category.DoesNotExist:
            print("Categoria associada ao perfil não encontrada.")
    