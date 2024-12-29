import requests
import logging
import os
import time
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

API_KEY = os.getenv('API_KEY')

logger = logging.getLogger(__name__)

class EmptyDataError(Exception):
  def __init__(self, s: str=""):
    super().__init__(s)

class UnknownIDError(Exception): 
  def __init__(self, s: str=""):
    super().__init__(s)

def get_competitions_ids() -> dict:
  uri = 'https://api.football-data.org/v4/competitions'
  headers = {'X-Auth-Token': API_KEY}
  response = requests.get(uri, headers=headers)
  response.raise_for_status() 
  competitions = response.json().get('competitions', {})
  result = None
  result = {str(c["id"]): c["name"] for c in competitions}
  if not result:
    raise EmptyDataError
  return result 

def get_current_season(id: str) -> dict:
  try:
    allowed_ids = get_competitions_ids()
  except requests.exceptions.RequestException as e:
    logger.warning("failed to fetch competitions IDs")
    raise e
  if not allowed_ids:
    logger.warning("got empty competitions IDs")
    raise EmptyDataError
  if id not in allowed_ids.keys():
    logger.warning(f"unknown id for competition lookup: {id}, allowed ids: {allowed_ids.keys()}")
    raise UnknownIDError
  uri = f'https://api.football-data.org/v4/competitions/{id}'
  headers = {'X-Auth-Token': API_KEY}
  response = requests.get(uri, headers=headers)
  response.raise_for_status() 
  current_season = response.json().get('currentSeason', {})
  return current_season
  
def get_competition_teams(competition_id: str, year: int = 2024) -> list:
   
    uri = f'https://api.football-data.org/v4/competitions/{competition_id}/teams?season={year}'
    headers = {'X-Auth-Token': API_KEY}
    try:
        response = requests.get(uri, headers=headers)
        response.raise_for_status()  
        teams = response.json().get('teams', [])
        if not teams:
            logger.warning(f"No teams found for competition {competition_id} in season {year}.")
            raise EmptyDataError("No teams found.")
        
        logger.info(f"Successfully fetched {len(teams)} teams for competition {competition_id}.")
        return teams
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch teams for competition {competition_id}: {str(e)}")
        raise e
    except KeyError as e:
        logger.error(f"Unexpected API response structure: {str(e)}")
        raise EmptyDataError("Unexpected response structure.")

def get_competition_standings(id: str, year: int=2024, type: str="TOTAL") -> dict:
  try:
    allowed_ids = get_competitions_ids()
  except requests.exceptions.RequestException as e:
    logger.warning("failed to fetch competitions IDs")
    raise e 
  if not allowed_ids:
    logger.warning("got empty competitions IDs")
    raise EmptyDataError
  if id not in allowed_ids.keys():
    logger.warning(f"unknown id for competition standings lookup: {id}, allowed ids: {allowed_ids.keys()}")
    raise UnknownIDError
  uri = f'https://api.football-data.org/v4/competitions/{id}/standings?season={year}'
  headers = {'X-Auth-Token': API_KEY}
  response = requests.get(uri, headers=headers)
  response.raise_for_status() 
  standings = response.json().get("standings")
  standings_filtered = None
  for standing in standings:
    if standing["type"] == type:
      standings_filtered = standing["table"]
  if not standings_filtered:
    raise EmptyDataError("Most likely unknown type")
  return standings_filtered

def get_team_players(id: str) -> dict:
    uri = f'https://api.football-data.org/v4/teams/{id}'
    headers = {'X-Auth-Token': API_KEY}
    try:
        response = requests.get(uri, headers=headers)
        response.raise_for_status()
        squad = response.json().get('squad', [])
        result = {
            player["id"]: {
                "name": player["name"],
                "position": player.get("position", "Unknown"),
                "dateOfBirth": player.get("dateOfBirth", None),
                "nationality": player.get("nationality", "Unknown"),
                "shirtNumber": player.get("shirtNumber", None),
            }
            for player in squad
        }
        time.sleep(3)  
        return result
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch players for team {id}: {e}")
        raise e

def get_player(id: str):
  uri = f'https://api.football-data.org/v4/persons/{id}'
  headers = {'X-Auth-Token': API_KEY}
  try:
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.warning(f"failed to fetch players' {id} data ({str(e)})")
    raise e
  return response.json()

def get_match(id: str):
  uri = f'https://api.football-data.org/v4/matches/{id}'
  headers = {'X-Auth-Token': API_KEY}
  try:
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.warning(f"failed to fetch matches' {id} data ({str(e)})")
    raise e
  return response.json()