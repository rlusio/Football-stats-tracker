from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),  
    path('all_players/', views.all_players, name='all_players'),  
    path('all_players/team/<int:team_id>/', views.team_players, name='team_players'),  
    path('all_players/top-market-value/', views.top_market_value, name='top_market_value'),
    path('all_players/top-performance-stats/', views.top_performance, name='top_performance'),
    path('details/<int:id>/', views.details, name='details'),  
    path('all_teams/', views.all_teams, name='all_teams'),  
    path('all_teams/team_details/<int:id>/', views.team_details, name='team_details'),
    path('all_matches/', views.all_matches, name='all_matches'),  
    path('all_matches/match_details/<int:id>/', views.match_details, name='match_details'),  
    path('user/', views.user, name='user'),
]
