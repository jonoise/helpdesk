from django.db import models
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from django.conf import settings
from .mensajitos import MENSAJITOS
import random
import datetime as dt

def attachments_upload_url(self, *args, **kwargs):
    return f'attachments/{self.ticket.owner}/{self.ticket.code}/attach.png'

# TODO : Borrar este código y hacer migraciones.
# class Account(models.Model):
#     is_user = models.BooleanField(default=False)
#     is_agent = models.BooleanField(default=False)


class Ticket(models.Model):

    DEPARTMENT_CHOICES = (
        ('front', 'Frontline'),
        ('back', 'Back-office'),
        ('wfm', 'Workforce'),
        ('it', 'IT'),
        ('management', 'Management'),
    )

    CATEGORY_CHOICES = (
        ('reunion', 'Sala de Reuniones'),
        ('ot', 'OT'),
        ('vto', 'VTO'),
        ('vacations', 'Vacaciones'),
        ('medic', 'Cita Médica'),
        ('insurance', 'Cita Aseguradora'),
    )

    STATUS_CHOICES = (
        ('pending', 'En espera'),
        ('ongoing', 'En curso'),
        ('closed', 'Cerrado'),
    )

    # Fields que el sistema va a llenar automáticamente.
    code = models.CharField(
        max_length=12, default=get_random_string, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='tickets')
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='assigned_tickets', blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Fields que el usuario va a suministrar.
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_escalated = models.BooleanField(
        verbose_name='es escalado', default=False, help_text="Marcarlo sólo si este issue ya fue atendido previamente.")
    subject = models.CharField(max_length=200, help_text="Escribe un título.")
    description = models.TextField(
        blank=False, help_text="Describe cuál es el problema.")

    def __str__(self):
        return f'code: {self.code} - date: {self.created}'

    def get_absolute_url(self):
        return reverse('helpdesk:ticket_detail', args=[self.created.year,
                                                       self.created.month,
                                                       self.created.day,
                                                       self.code])


class Comment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField(
        verbose_name='content', blank=False, help_text="Escribe aquí tu mensaje.")

    def __str__(self):
        return f'from {self.owner} on ticket #{self.ticket.code}'


class Attachment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attachments')
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='attachments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=attachments_upload_url, blank=True)
    file = models.FileField(upload_to=attachments_upload_url, blank=True)
    description = models.TextField(
        blank=False, help_text="Describe el propósito de la imagen.")


class Log(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='logs')
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=200)
    header = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    def __str__(self):
        return f'user: {self.user}, {self.ticket} - {self.date}'


class VacationRequest(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacation_requests')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    from_date = models.DateField(verbose_name="from")
    to_date = models.DateField(verbose_name="to")
    status = models.CharField(
        max_length=20, choices=Ticket.STATUS_CHOICES, default="pending")
    
    def __str__(self):
        return f'owner: {self.owner} - {self.status}'
    

class Vacation(models.Model):
    VACATION_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacations')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    from_date = models.DateField(verbose_name="from")
    to_date = models.DateField(verbose_name="to")
    status = models.CharField(max_length=20, choices=VACATION_STATUS, default='pending')
    mensajito = models.CharField(max_length=300, default=f''.join(random.choices(MENSAJITOS)))
    
    def __str__(self):
        return f'owner: {self.owner} - {self.status}'
    
    
