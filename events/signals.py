from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

import logging

from events.models import Availability, Cancellation, Team
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




@receiver(post_save, sender=Team)
def create_payments_for_team(sender, instance, **kwargs):
    """Cria pagamentos para disponibilidades convocadas quando o status do time for atualizado para True."""
    if instance.status:  
        availabilities = Availability.objects.filter(team=instance, summoned=True, status=True)
        for availability in availabilities:
            try:
                logger.info("[Signal-create-payments-for-team] Triggered for availability summoned and team status active.")

                payment = Payment.objects.filter(event=instance.event, profile=availability.profile)
                if payment.exists():
                    logger.info(f"Pagamento já existe para o perfil {availability.profile} e o evento {instance.event}.")
                    payment.update(status="PENDING")
                    continue  

                category = availability.profile.category
                base_amount = category.amount
                percentage_multiplier = Decimal(category.percentage / 100)
                total_category_payment = base_amount + (base_amount * percentage_multiplier)

                daily_rate = instance.event.daily or Decimal(0)
                payment_amount = total_category_payment * daily_rate

                Payment.objects.create(
                    event=instance.event,
                    profile=availability.profile,
                    amount=payment_amount
                )

            except Category.DoesNotExist:
                logger.error("Categoria associada ao perfil não encontrada.")
            except Exception as e:
                logger.error(f"Erro ao calcular pagamento: {e}")



@receiver(post_save, sender=Availability)
def create_payment_for_resurrected_availability(sender, instance, **kwargs):
    """Cria pagamentos para disponibilidades ressuscitadas (summoned=True) ou para novas disponibilidades,
       apenas se o time estiver fechado (evento fechado)."""

    if instance.summoned and instance.status:
        try:
            team = instance.team
            if not team.status:  
                logger.info(f"Evento {team.name} não está fechado, pagamento não será criado.")
                return  
            
            payment = Payment.objects.filter(event=team.event, profile=instance.profile)

            if payment.exists():
                logger.info(f"Pagamento já existe para o perfil {instance.profile} e o evento {team.event}.")
    
                payment.update(status="PENDING")  
                return 

            # Calcula o pagamento usando a categoria do perfil
            category = instance.profile.category
            base_amount = category.amount
            percentage_multiplier = Decimal(category.percentage / 100)
            total_category_payment = base_amount + (base_amount * percentage_multiplier)

            daily_rate = team.event.daily or Decimal(0)
            payment_amount = total_category_payment * daily_rate

            # Cria o pagamento
            Payment.objects.create(
                event=team.event,
                profile=instance.profile,
                amount=payment_amount
            )
            logger.info(f"Pagamento criado para o perfil {instance.profile} e o evento {team.event}.")

        except Category.DoesNotExist:
            logger.error("Categoria associada ao perfil não encontrada.")
        except Exception as e:
            logger.error(f"Erro ao calcular pagamento: {e}")


@receiver(post_delete, sender=Availability)
def remove_payment_for_deleted_availability(sender, instance, **kwargs):
    """Remove o pagamento associado ao Availability quando ele for excluído."""
    try:
        payment = Payment.objects.filter(event=instance.team.event, profile=instance.profile)
        
        if payment.exists():
            payment.delete() 
            logger.info(f"Pagamento removido para o perfil {instance.profile} e o evento {instance.team.event}.")
        else:
            logger.info(f"Nenhum pagamento encontrado para o perfil {instance.profile} e o evento {instance.team.event}.")
    
    except Exception as e:
        logger.error(f"Erro ao tentar remover o pagamento: {e}")

