import scripts.api as api
import csv
import logging
from time import sleep
import json
logger = logging.getLogger(__name__)

def scrape_competitions_ids():
    data = api.get_competitions_ids()
    print(data)
    with open("competitions_ids.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'Competition'])
        for key, value in data.items():
            writer.writerow([key, value])

def scrape_seasons():
    ids = api.get_competitions_ids()
    data = {}
    fieldnames = ['id', 'startDate', 'endDate', 'currentMatchday', 'winner']
    with open("seasons.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for id in ids:
            try:
                sleep(10)
                print(f"Fetching season {id}")
                season_data = api.get_current_season(str(id))
                data_to_write = {
                    'id': id,
                    'startDate': season_data.get('startDate', ''),
                    'endDate': season_data.get('endDate', ''),
                    'currentMatchday': season_data.get('currentMatchday', ''),
                    'winner': season_data.get('winner', '')
                }
                logger.debug(f"Got season data: {data_to_write}")
                writer.writerow(data_to_write)
                data[id] = season_data
            except api.UnknownIDError:
                logger.debug(f"Season with ID {id} not found.")
            except Exception as e:
                logger.error(f"Error fetching season {id}: {str(e)}")
    
def scrape_competitions_teams():
    ids = []
    with open("seasons.csv", mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append(row['id'])
    data = {}
    for id in ids:
        try:
            data[id] = api.get_competition_teams(id)
            logger.debug(f"saved ID: {id}")
            sleep(10)
        except Exception as e:
            logger.debug(e)
            sleep(10)
    with open("competition_teams.json", mode='w', newline='', encoding='utf-8') as file:
        json.dump(data, file)

def scrape_competition_standings():
    ids = []
    with open("seasons.csv", mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append(row['id'])
    data = {}
    
    for id in ids:
        try:
            data[id] = api.get_competition_standings(id)
            logger.debug(f"saved ID: {id}")
            sleep(10)
        except Exception as e:
            logger.debug(e)
            sleep(10)
        with open("competition_standings.json", mode='w', newline='', encoding='utf-8') as file:
            json.dump(data, file)

def scrape_players():  
    with open('competition_teams.json', 'r') as file:
        data_teams = json.load(file)
    player_ids = []

    for year, teams in data_teams.items():
        for team in teams:
            squad = team.get('squad', [])
            for player in squad:
                player_ids.append(player['id'])

    with open("players_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["id", "data"])
        for id in player_ids:
            try:
                d = api.get_player_stats(id)
                logger.debug(f"saved id: {id}")
                sleep(7) 
                csv_writer.writerow([id, json.dumps(d)])  
                csvfile.flush()
            except Exception as e:
                logger.debug(f"Error {id}: {e}")
    
if __name__ == "__main__":
    pass