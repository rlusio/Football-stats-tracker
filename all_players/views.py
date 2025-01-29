from all_players.models import Player, Team, Match
from django.shortcuts import render, get_object_or_404


def top_market_value(request):
    players = Player.objects.all()
    below_5m = players.filter(marketValue__lt=5000000)
    between_5m_20m = players.filter(marketValue__gte=5000000, marketValue__lt=20000000)
    above_20m = players.filter(marketValue__gte=20000000)

    # print(f"Below $5M: {below_5m}")
    # print(f"$5M–$20M: {between_5m_20m}")
    # print(f"Over $20M: {above_20m}")

    context = {
        'below_5m': below_5m,
        'between_5m_20m': between_5m_20m,
        'above_20m': above_20m,
    }
    return render(request, 'all_players/top_market_value.html', context)


def top_performance(request):
    players = Player.objects.all()
    top_scorers = players.filter(goals__gt=10)
    top_assisters = players.filter(assists__gt=5)

    context = {
        'top_scorers': top_scorers,
        'top_assisters': top_assisters,
    }
    return render(request, 'all_players/top_performance.html', context)


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
