from django.shortcuts import render, redirect
from .models import Ticket, Comment, Attachment, Log, VacationRequest, Vacation
from .forms import TicketForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'helpdesk/index.html')

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(owner=request.user)
    comments = Comment.objects.filter(owner=request.user)

    context = {
        'tickets': tickets,
        'comments': comments,
    }

    return render(request, 'helpdesk/dashboard.html', context)

@login_required
def new_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('helpdesk:dashboard')


@login_required
def ticket_detail(request, year, month, day, code):
    ticket = get_object_or_404(Ticket(created__year=year,
                                      created__month=month,
                                      created__day=day,
                                      code=code))
    comments = ticket.comments.all()
    logs = ticket.logs.all()
    attachments = ticket.attachments.all()

    context = {
        'ticket': ticket,
        'comments': comments,
        'logs': logs,
    }

    return render(request, 'helpdesk/detail.html', context)
