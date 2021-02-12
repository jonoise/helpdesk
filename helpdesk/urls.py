from django.urls import path
from . import views

app_name = 'helpdesk'
urlpatterns = [
    path('', views.index, name='index'),
    path('helpdesk/', views.helpdesk, name='helpdesk'),
    path('<int:year>/<int:month>/<int:day>/<str:code>',
         views.helpdesk, name='ticket_detail'),
    
]
