from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),  
    path('all_players/', views.all_players, name='all_players'),  
    path('all_players/team/<int:team_id>/', views.all_players, name='team_players'),
    path('details/<int:id>/', views.details, name='details'),  
    path('all_teams/', views.all_teams, name='all_teams'),  
    path('all_teams/team_details/<int:id>/', views.team_details, name='team_details'),
    path('all_matches/', views.all_matches, name='all_matches'),  
    path('all_matches/match_details/<int:id>/', views.match_details, name='match_details'),  
    path('user/',views.user, name = 'user'),
    path('user/viewed_items/', views.viewed_items, name='viewed_items'),
    path('user/viewed_teams/', views.viewed_teams, name='viewed_teams'),
    path('user/viewed_players/', views.viewed_players, name='viewed_players'),
]