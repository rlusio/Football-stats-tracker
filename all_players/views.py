from .models import Player
from django.http import HttpResponse
from django.template import loader
from .models import Player
from .models import Team
from .models import Match
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

def all_teams(request):
    myteams =Team.objects.all().values()
    template = loader.get_template('all_teams/all_teams.html')
    context={
        'myteams': myteams,
        }
    return HttpResponse(template.render(context, request))
def team_details(request,id):
    myteam =Team.objects.get(id=id)
    template = loader.get_template('all_teams/team_details.html')
    context={
        'myteam': myteam,
        }
    return HttpResponse(template.render(context, request))

def all_matches(request):
    mymatches =Match.objects.all().values()
    template = loader.get_template('all_matches/all_matches.html')
    context={
        'mymatches': mymatches,
        }
    return HttpResponse(template.render(context, request))
def match_details(request,id):
    mymatch = Match.objects.all().get(id=id)
    template = loader.get_template('all_matches/match_details.html')
    context={
        'mymatch': mymatch,
        }
    return HttpResponse(template.render(context, request))

def main(request):
    return render(request, 'main/home.html')

