from .models import Player, Team, Match
from django.shortcuts import render, get_object_or_404

def all_players(request):
    myplayers = Player.objects.all() 
    return render(request, 'all_players/all_players_info.html', {'myplayers': myplayers})

def details(request, id):
    myplayer = get_object_or_404(Player, id=id) 
    return render(request, 'details.html', {'myplayer': myplayer})

def all_teams(request):
    myteams = Team.objects.all()
    return render(request, 'all_teams/all_teams.html', {'myteams': myteams})

def team_details(request, id):
    myteam = get_object_or_404(Team, id=id)
    return render(request, 'all_teams/team_details.html', {'myteam': myteam})

def all_matches(request):
    mymatches = Match.objects.all()
    return render(request, 'all_matches/all_matches.html', {'mymatches': mymatches})

def match_details(request, id):
    mymatch = get_object_or_404(Match, id=id) 
    return render(request, 'all_matches/match_details.html', {'mymatch': mymatch})

def user(request):
    return render(request, 'user/user.html')

def main(request):
    return render(request, 'main/home.html')