from all_players.models import Player, Team, Match
from django.shortcuts import render, get_object_or_404

def all_players(request, team_id=None):
    if team_id:
        team = get_object_or_404(Team, id=team_id)
        
        myplayers = Player.objects.filter(team__Team_Name=team.Team_Name)
    else:
        myplayers = Player.objects.all()
    return render(request, 'all_players/all_players_info.html', {'players': myplayers})

def team_players(request, team_id):
    myplayers = Player.objects.filter(team=team_id)  
    return render(request, 'all_players/all_players_info.html', {'players': myplayers})

def details(request, id):
    myplayer = get_object_or_404(Player, id=id) 
    return render(request, 'all_players/details.html', {'myplayer': myplayer})


def all_teams(request):
    myteams = Team.objects.all()
    return render(request, 'all_teams/all_teams.html', {'myteams': myteams})

def team_details(request, id):
    myteam = get_object_or_404(Team, id=id)
 
    viewed_teams = request.session.get('viewed_teams', [])
    if id not in viewed_teams:
        viewed_teams.append(id)
        if len(viewed_teams) > 10:
            viewed_teams.pop(0)
    request.session['viewed_teams'] = viewed_teams 

    return render(request, 'all_teams/team_details.html', {'myteam': myteam})

def all_matches(request):
    mymatches = Match.objects.all()
    return render(request, 'all_matches/all_matches.html', {'mymatches': mymatches})

def match_details(request, id):
    mymatch = get_object_or_404(Match, id=id)
    viewed_matches = request.session.get('viewed_matches', [])
    if id not in viewed_matches:
        viewed_matches.append(id)
        if len(viewed_matches) > 10:
            viewed_matches.pop(0)
    request.session['viewed_matches'] = viewed_matches     
    return render(request, 'all_matches/match_details.html', {'mymatch': mymatch})

def user(request):
    return render(request, 'user/user.html')

def viewed_items(request):
    viewed_matches_ids = request.session.get('viewed_matches', [])
    viewed_matches = Match.objects.filter(id__in=viewed_matches_ids)
    return render(request, 'user/viewed_items.html', {'viewed_matches': viewed_matches})


def viewed_teams(request):
    viewed_teams_ids = request.session.get('viewed_teams', [])
    viewed_teams = Team.objects.filter(id__in=viewed_teams_ids)
    return render(request, 'user/viewed_teams.html', {'viewed_matches': viewed_teams})

def viewed_players(request):
    viewed_players_ids = request.session.get('viewed_players', [])
    viewed_players = Player.objects.filter(id__in=viewed_players_ids)
    return render(request, 'user/viewed_players.html', {'viewed_player': viewed_players})



def main(request):
    return render(request, 'main/home.html')