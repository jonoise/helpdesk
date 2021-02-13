from django.contrib import admin
from .models import MyUser, Rol, Account


# Register your models here.

admin.site.register(MyUser)
admin.site.register(Rol)
admin.site.register(Account)
    
