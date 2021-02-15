from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MyUserCreationForm, RolForm, EditAccountForm
from .models import MyUser, Account

# Create your views here.

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
    form = RolForm(instance=request.user.account.rol)
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('helpdesk:helpdesk')