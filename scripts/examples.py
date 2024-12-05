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

if __name__ == "__main__":
    current_season()