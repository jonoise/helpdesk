from django.contrib import admin
from .models import Ticket, Comment, Attachment, Log, Vacation


# admin.site.register(Ticket)
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'owner', 'agent', 'created', 'status')
    list_filter = ('owner', 'created', 'status')
    search_filter = ('subject', 'description')
    date_hierarchy = 'created'


admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Log)
admin.site.register(Vacation)
