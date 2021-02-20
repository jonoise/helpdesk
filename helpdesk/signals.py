from django.db.models.signals import post_save
from .models import Ticket, Vacation
from django.dispatch import receiver

@receiver(post_save, sender=Ticket)
def vacationRequest(sender, instance, created, **kwargs):
    if created and instance.category == 'Vacations':
        vac = Vacation.objects.create(ticket=instance, owner=instance.owner)
        vac.save()
    else:
        pass