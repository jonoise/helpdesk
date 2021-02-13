from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def account_image_upload_url(self, *args, **kwargs):
    return f'account_images/{self.owner}/profile.png'

def default_image_upload_url(self, *args, **kwargs):
    return f'account_images/default.png'

class MyUser(AbstractUser):
    pass

class Account(models.Model):
    owner = models.OneToOneField(MyUser, verbose_name='account', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=account_image_upload_url, default="")

    def __str__(self):
        return f'{self.owner.username} account'.title()
    

class Rol(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_regular = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)

    def check_user_role(self):
        if self.user.is_regular:
            return 'Regular'
        else:
            return 'Agent'

    def __str__(self):
        if self.user.rol.is_regular:
            return f'{self.user} es regular'.title()
        elif self.user.rol.is_agent:
            return f'{self.user} es agente'.title()
        else:
            return f'{self.user}, sin asignar'.title()