from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_players, name='all_players'),
    path('all_players/', views.all_players, name='all_players'),
    path('details/<int:id>/', views.details,name='details'),
    path('all_matches/', views.all_matches, name='all_matches'),
    path('all_teams/', views.all_teams, name='all_teams'),
    
]