from django.db.models.signals import post_save
from .models import MyUser, Account, Rol
from django.dispatch import receiver

@receiver(post_save, sender=MyUser)
def accountProfile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(owner=instance)
        Rol.objects.create(user=instance)
        

@receiver(post_save, sender=MyUser)
def save_account(sender, instance, **kwargs):
    instance.account.save()
    instance.rol.save()