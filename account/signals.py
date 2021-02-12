from django.db.models.signals import post_save
from .models import MyUser, Account
from django.dispatch import receiver

@receiver(post_save, sender=MyUser)
def accountProfile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(owner=instance)

@receiver(post_save, sender=MyUser)
def save_account(sender, instance, **kwargs):
    instance.account.save()