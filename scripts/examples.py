from api import *

def current_season():
    print(get_current_season('2014'))

def competition_teams():
    competitions = get_competition_teams('2014')
    print([c['name'] for c in competitions])

def comp_standings():
    response_data = get_competition_standings('2021')
    for data in response_data:
        print(f"{data['position']}. ({data['points']}p): {data['team'].get('name')}")

def player():
    p = get_player('421')
    print(p)

def team_players():
    t = get_team_players('112')
    print(t)

def player_matches():
    t = get_player_stats('16275')
    print(t)

def match_stats():
    t = get_match_stats('2021', 2024)
    print(t)
    
if __name__ == "__main__":
    player_matches()