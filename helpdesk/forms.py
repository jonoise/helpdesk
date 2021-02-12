from django import forms
from .models import Ticket, Comment, Attachment, VacationRequest

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('department', 'category', 'is_escalated', 'subject', 'description')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('image', 'file', 'description')

class VacationRequestForm(forms.ModelForm):
    class Meta:
        model = VacationRequest
        fields = ('from_date', 'to_date')


