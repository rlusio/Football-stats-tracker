import api
import json

def current_season():
    print(api.get_current_season('2014'))

def competition_teams():
    competitions = api.get_competition_teams('2014')
    print([c['name'] for c in competitions])

def comp_standings():
    response_data = api.get_competition_standings('2021')
    for data in response_data:
        print(f"{data['position']}. ({data['points']}p): {data['team'].get('name')}")

def player():
    p = api.get_player('421')
    print(p)

def team_players():
    t = api.get_team_players('112')
    print(t)

def player_matches():
    t = api.get_player_stats('16275')
    print(t)

def match_stats():
    t = api.get_match_stats('2021', 2024)
    print(t)
    
if __name__ == "__main__":
    print(api.get_player_stats("171893"))