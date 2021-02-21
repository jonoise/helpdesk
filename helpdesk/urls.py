from django.urls import path
from . import views

app_name = 'helpdesk'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new-ticket/', views.new_ticket, name='new_ticket'),
    path('vacation-list', views.vacation_list, name='vacation_list'),
    path('vacation-request/<str:code>/', views.vacation_request, name='vacation_request'),
    path('unassigned/', views.unassigned_tickets, name='unassigned'),
    path('ticket/<int:year>/<int:month>/<int:day>/<str:code>/',
         views.ticket_detail, name='ticket_detail'),

    # assigning tickets to agents
    path('take-ticket/<str:code>/', views.take_ticket, name="take_ticket"),

    #comment_handling
    path('comment-handling/<str:code>/<int:pk>/', views.comment_handling, name='comment_handling'),
    
    #ticket_decision_handling
    path('ticket-decision-handling/<str:code>', views.ticket_decision_handling, name='ticket_decision_handling'),
    
    #vacation_decision_handling
    path('vacation-decision-handling/<str:code>', views.vacation_decision_handling, name='vacation_decision_handling'),
]