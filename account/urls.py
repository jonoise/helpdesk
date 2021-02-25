from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'account'
urlpatterns = [
    path('create/', views.create_user, name='create'),
    path('edit/', views.edit, name='edit'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('rol/', views.user_rol, name='rol'),
]
