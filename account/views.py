from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm
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
            return redirect('helpdesk:index')

    context = {
        'form':form
    }
    return render(request, 'account/create.html', context)

@login_required
def detail(request):
    user = get_object_or_404(MyUser, username=request.user.username)

    context = {
        'user':user
    }

    return render(request, 'account/detail.html', context)

def user_rol(request):
    pass