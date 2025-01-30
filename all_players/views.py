from all_players.models import Player, Team, Match, Standing
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Sum, Q
from datetime import date
import os
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render
from .models import Player

def top_market_value(request):
    players = Player.objects.all()
    below_5m = players.filter(marketValue__lt=5000000)
    between_5m_20m = players.filter(marketValue__gte=5000000, marketValue__lt=20000000)
    above_20m = players.filter(marketValue__gte=20000000)
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
    filename = f"{myplayer.firstname} {myplayer.lastname}_stats.png"
    plot_path = f"player_plots/{filename}"
    return render(request, 'all_players/details.html', {'myplayer': myplayer,'plot_path': plot_path})

def all_teams(request):
    myteams = Team.objects.all()
    return render(request, 'all_teams/all_teams.html', {'myteams': myteams})

def top_wins(request):
    players = Player.objects.annotate(
        wins=Count('team__wins')
    ).order_by('-wins')
    return render(request, 'all_players/top_wins.html', {'players': players})

def team_details(request, id):
    myteam = Team.objects.filter(id=id).first()
    teamstandings = Standing.objects.filter(team=myteam).order_by('-season').first()
    num_players = Player.objects.filter(team=myteam).count()
    total_goals = Player.objects.filter(team=myteam).aggregate(Sum('goals'))['goals__sum']
    players = Player.objects.filter(team=myteam).exclude(dateOfBirth=None)
    avg_age = None
    if players.exists():
        current_year = date.today().year
        avg_age = sum(current_year - player.dateOfBirth.year for player in players) / players.count()
    return render(request, 'all_teams/team_details.html', {
        'myteam': myteam, 'mystandings': teamstandings,'num_players': num_players, 'total_goals': total_goals,'avg_age': round(avg_age, 1) if avg_age else "N/A"  })
    
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

def by_position(request):
    positions = Player.objects.values_list('position', flat=True).distinct()  
    return render(request, 'all_players/by_position.html', {'positions': positions})

def players_by_position(request, position):
    players = Player.objects.filter(position=position) 
    return render(request, 'all_players/players_by_position.html', {'players': players, 'position': position})

