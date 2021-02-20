from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Account, Rol

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'first_name')

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('image', 'description', 'facebook', 'instagram', 'twitter')

class RolForm(forms.Form):
    ROL_CHOICES = (
        ('Regular', 'Regular'),
        ('Agent', 'Agent'),
    )

    rol = forms.ChoiceField(choices=ROL_CHOICES, widget=forms.RadioSelect)