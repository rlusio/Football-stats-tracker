from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),  
    path('all_players/', views.all_players, name='all_players'),  
    path('all_players/team/<int:team_id>/', views.team_players, name='team_players'),  
    path('all_players/by-position/', views.by_position, name='by_position'),
    path('all_players/by-position/<str:position>/', views.players_by_position, name='players_by_position'),
    path('all_players/by-nationality/', views.by_nationality, name='by_nationality'),
    path('all_players/by-nationality/<str:nationality>/', views.players_by_nationality, name='players_by_nationality'),
    path('details/<int:id>/', views.details, name='details'),  
    path('all_teams/', views.all_teams, name='all_teams'),  
    path('all_teams/team_details/<int:id>/', views.team_details, name='team_details'),
    path('all_matches/', views.all_matches, name='all_matches'),  
    path('all_matches/match_details/<int:id>/', views.match_details, name='match_details'),  
    path('user/', views.user, name='user'),
]
