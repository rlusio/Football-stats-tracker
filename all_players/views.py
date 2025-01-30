from all_players.models import Player, Team, Match, Standing
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Sum
from datetime import date
<<<<<<< HEAD
import os
import matplotlib.pyplot as plt
from django.conf import settings
=======
>>>>>>> 332d52b82a11a0e63b87edba54c89ed99ffcbec4

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

<<<<<<< HEAD
def generate_team_chart(team_id, won, lost, draw):
    chart_dir = os.path.join(settings.BASE_DIR, 'mystaticfiles/charts')
    os.makedirs(chart_dir, exist_ok=True)  
    chart_filename = f"team_{team_id}_chart.png"
    chart_path = os.path.join(chart_dir, chart_filename)
    labels = ['Wins', 'Losses', 'Draws']
    values = [won, lost, draw]
    colors = ['green', 'red', 'orange']
    plt.figure(figsize=(5, 4))
    plt.bar(labels, values, color=colors)
    plt.title("Match Results")
    plt.ylabel("Number of Matches")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()  
    return f"charts/{chart_filename}"

=======
>>>>>>> 332d52b82a11a0e63b87edba54c89ed99ffcbec4
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

<<<<<<< HEAD
=======
def top_wins(request):
    players = Player.objects.annotate(
        wins=Count('team__wins')
    ).order_by('-wins')

    return render(request, 'all_players/top_wins.html', {'players': players})


>>>>>>> 332d52b82a11a0e63b87edba54c89ed99ffcbec4
def team_details(request, id):
    myteam = Team.objects.filter(id=id).first()
    teamstandings = Standing.objects.filter(team=myteam).order_by('-season').first()
    num_players = Player.objects.filter(team=myteam).count()
    total_goals = Player.objects.filter(team=myteam).aggregate(Sum('goals'))['goals__sum']
    players = Player.objects.filter(team=myteam).exclude(dateOfBirth=None)
    avg_age = None
<<<<<<< HEAD

    won = teamstandings.won if teamstandings else 0
    lost = teamstandings.lost if teamstandings else 0
    draw = teamstandings.draw if teamstandings else 0
    chart_url = generate_team_chart(id, won, lost, draw)
=======
>>>>>>> 332d52b82a11a0e63b87edba54c89ed99ffcbec4
    if players.exists():
        current_year = date.today().year
        avg_age = sum(current_year - player.dateOfBirth.year for player in players) / players.count()
    return render(request, 'all_teams/team_details.html', {
<<<<<<< HEAD
        'myteam': myteam, 'mystandings': teamstandings,'num_players': num_players, 'total_goals': total_goals,'avg_age': round(avg_age, 1) if avg_age else "N/A"  ,'chart_url': chart_url})
=======
        'myteam': myteam, 'mystandings': teamstandings,'num_players': num_players, 'total_goals': total_goals,'avg_age': round(avg_age, 1) if avg_age else "N/A"  })
>>>>>>> 332d52b82a11a0e63b87edba54c89ed99ffcbec4
    
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
<<<<<<< HEAD
=======

from django.shortcuts import render
from .models import Player

def by_position(request):
    positions = Player.objects.values_list('position', flat=True).distinct()  # Pobiera unikalne pozycje
    return render(request, 'all_players/by_position.html', {'positions': positions})

def players_by_position(request, position):
    players = Player.objects.filter(position=position)  # Pobiera graczy na danej pozycji
    return render(request, 'all_players/players_by_position.html', {'players': players, 'position': position})

def by_nationality(request):
    nationalities = Player.objects.values_list('nationality', flat=True).distinct()  # Pobiera unikalne narodowości
    return render(request, 'all_players/by_nationality.html', {'nationalities': nationalities})

def players_by_nationality(request, nationality):
    players = Player.objects.filter(nationality=nationality)  # Pobiera graczy danej narodowości
    return render(request, 'all_players/players_by_nationality.html', {'players': players, 'nationality': nationality})
>>>>>>> 332d52b82a11a0e63b87edba54c89ed99ffcbec4
