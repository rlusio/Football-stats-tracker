from .models import Player
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def all_players(request):
    myplayers = Player.objects.all()
    return render(request, 'all_players/all_players_info.html', {'myplayers': myplayers})

def details(request,id):
    myplayer=Player.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myplayer': myplayer,
         }
    return HttpResponse(template.render(context,request))

def main(request):
    return render(request, 'main/home.html')

