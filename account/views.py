from helpdesk.models import Log
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MyUserCreationForm, RolForm, EditAccountForm
from .models import MyUser, Account
from helpdesk.models import Log
from .logs import rol_Log



def create_user(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = MyUser(
                username = request.POST['username'],
                password = request.POST['password2'],
                first_name = request.POST['first_name'],
            )
            new_user.save()
            message = messages.success(request, 'Usuario, creado')
            return redirect('account:rol', messages=message)

    context = {
        'form':form
    }
    return render(request, 'account/create.html', context)


def login(request):
    pass

@login_required
def edit(request):
    user = get_object_or_404(MyUser, username=request.user.username)
    form = EditAccountForm(instance=user.account)
    
    if request.method == 'POST':
        form = EditAccountForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('helpdesk:helpdesk')

    context = {
        'form':form
    }

    return render(request, 'account/edit.html', context)




@login_required()
def user_rol(request):
    if request.user.rol.is_agent:
        form = RolForm(initial={'rol':'Agent'})
    elif request.user.rol.is_regular:
        form = RolForm(initial={'rol':'Regular'})
    else:
        form = RolForm()
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            rol = form.cleaned_data['rol']
            if rol == 'Agent':
                request.user.rol.is_agent = True
                request.user.rol.is_regular = False
                request.user.rol.save()
                rol_Log(rol, Log, request.user)
                
            if rol == 'Regular':
                request.user.rol.is_agent = False
                request.user.rol.is_regular = True
                request.user.rol.save()
                rol_Log(Log, request.user, rol)
                
            return redirect('helpdesk:helpdesk')

    return render(request, 'account/rol.html', {'form':form})