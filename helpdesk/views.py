# Módulos de django
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
# Mis módulos
from account.models import MyUser
from .models import Ticket, Comment, Vacation
from .forms import (
    TicketForm, 
    CommentForm, 
    AttachmentForm, 
    VacationRequestForm, 
    VacationDecisionForm, 
    TicketDecisionForm
)


def index(request):
    return render(request, 'helpdesk/index.html')

@login_required
def dashboard(request):
    # Variables depediendo del usuario.
    if request.user.rol.is_regular:
        tickets = Ticket.objects.filter(owner=request.user)
        vacations = Vacation.objects.filter(owner=request.user)
    elif request.user.rol.is_agent:
        tickets = Ticket.objects.filter(agent=request.user)
        vacations = Vacation.objects.filter(agent=request.user)

    comments = Comment.objects.filter(owner=request.user)
    pending_vacations = vacations.filter(status='pending')
    approved_vacations = vacations.filter(status='approved')

    context = {
        'tickets': tickets,
        'comments': comments,
        'vacations': vacations,
        'pending_vacations': pending_vacations,
        'approved_vacations': approved_vacations,
    }

    return render(request, 'helpdesk/dashboard.html', context)

@login_required
def new_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            # Si la categoría es Vacaciones lo envía al view vacation_request (definido más abajo)
            if form.category == 'Vacations':
                return redirect('helpdesk:vacation_request', form.code)
            return redirect('helpdesk:dashboard')
    
    return render(request, 'helpdesk/new_ticket.html', {'form':form})

@login_required
def ticket_detail(request, year, month, day, code):
    # Se obtienen las 2 principales piezas de información:
    user = request.user
    ticket = get_object_or_404(Ticket, created__year=year,
                                      created__month=month,
                                      created__day=day,
                                      code=code)
    
    # Se asegura que el usuario que intenta acceder a un ticket
    # sea el owner o el agent asignado a ese ticket:
    if ticket.owner == user or ticket.agent == user:
        comments = ticket.comments.all()
        attachments = ticket.attachments.all()    
        comment_form = CommentForm()
        attachment_form = AttachmentForm()
        

        context = {
            'ticket': ticket,
            'comments': comments,
            'attachments': attachments,
            'comment_form': comment_form,
            'attachment_form': attachment_form,
        }

        
        # Se agregan variables extras para renderizar SOLO
        # si el usuario es agente:
        if ticket.agent == user:
            ticket_decision_form = TicketDecisionForm(instance=ticket)
            context['ticket_decision_form'] = ticket_decision_form
            if len(ticket.vacations.all()) == 1:
                vacation = ticket.vacations.get(ticket__code=code)
                vacation_decision_form = VacationDecisionForm(instance=vacation)
                context['vacation_decision_form'] = vacation_decision_form
                context['vacation'] = vacation

        if request.method == 'POST':
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.owner = request.user
                form.ticket = ticket
                form.save()
                return redirect(
                    'helpdesk:ticket_detail', 
                    ticket.created.year, 
                    ticket.created.month, 
                    ticket.created.day, 
                    ticket.code
                )

        return render(request, 'helpdesk/detail.html', context)

    # si es usuario no es el dueño del ticket o el agente asignado:
    return redirect('helpdesk:dashboard')

@login_required
def unassigned_tickets(request):
    # solo agentes pueden ver los tickets sin asignar.
    if request.user.rol.is_agent:

        tickets = Ticket.objects.filter(agent=None)

        return render(request, 'helpdesk/unassigned.html', {'tickets':tickets})
    else:
        return redirect('helpdesk:dashboard')

@login_required
def take_ticket(request, code):
    if request.user.rol.is_agent:
        ticket = get_object_or_404(Ticket, code=code)
        ticket.agent = request.user
        ticket.save()
        # si es una vacación vamos a asignarle ser el agente de la vacación también.
        if ticket.category == 'Vacations':
            vacation = ticket.vacations.get(ticket__code=code)
            vacation.agent = request.user
            vacation.save()

        return redirect('helpdesk:dashboard')
    else:
        return redirect('helpdesk:dashboard')

@login_required
def vacation_request(request, code):
    vacation = Vacation.objects.get(ticket__code=code)
    form = VacationRequestForm(instance=vacation)
    if request.method == 'POST':
        form = VacationRequestForm(request.POST, instance=vacation)
        if form.is_valid():
            form.save()
            return redirect('helpdesk:dashboard')
    
    return render(request, 'helpdesk/vacation_new.html', {'form':form})

@login_required
def vacation_list(request):
    vacations = Vacation.objects.filter(owner=request.user)

    return render(request, 'helpdesk/vacation_list.html', {'vacations':vacations})

@login_required
def comment_handling(request, code, pk):
    if request.method == 'POST':
        user = get_object_or_404(MyUser, pk=pk)
        ticket = get_object_or_404(Ticket, code=code)
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = user
            form.ticket = ticket
            form.save()
            # Los argumentos extra son los necesarios para obtener
            # el AbsoluteURL del ticket en el que se acaba de comentar.
            return redirect('helpdesk:ticket_detail', ticket.created.year, ticket.created.month, ticket.created.day, ticket.code)

@login_required
def ticket_decision_handling(request, code):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, code=code)
        form = TicketDecisionForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            # Los argumentos extra son los necesarios para obtener
            # el AbsoluteURL del ticket en el que se acaba de comentar.
            return redirect('helpdesk:ticket_detail', ticket.created.year, ticket.created.month, ticket.created.day, ticket.code)

@login_required
def vacation_decision_handling(request, code):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, code=code)
        vacation = ticket.vacations.get(ticket__code=code)
        form = VacationDecisionForm(request.POST, instance=vacation)
        if form.is_valid():
            form.save()
            # Los argumentos extra son los necesarios para obtener
            # el AbsoluteURL del ticket en el que se acaba de comentar.
            return redirect('helpdesk:ticket_detail', ticket.created.year, ticket.created.month, ticket.created.day, ticket.code)
