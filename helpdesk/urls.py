from django.urls import path
from . import views

app_name = 'helpdesk'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='helpdesk'),
    path('new-ticket/', views.new_ticket, name='new_ticket'),
    path('<int:year>/<int:month>/<int:day>/<str:code>',
         views.ticket_detail, name='ticket_detail'),
    
]
