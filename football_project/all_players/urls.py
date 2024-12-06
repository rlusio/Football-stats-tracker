from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('all_players/', views.all_players, name='all_players'),
    path('all_players/details/<int:id>', views.details,name='details'),
    
]