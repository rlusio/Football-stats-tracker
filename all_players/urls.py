from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_players, name='all_players'),
    path('details/<int:id>/', views.details,name='details'),
    
]