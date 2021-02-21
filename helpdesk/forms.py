from django import forms
from .models import Ticket, Comment, Attachment, Vacation
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('owner', 'agent', 'department', 'category', 'is_escalated', 'subject', 'description')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('image', 'description')

class VacationRequestForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ('from_date', 'to_date')

class VacationDecisionForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ('status',)

class TicketDecisionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('status',)

