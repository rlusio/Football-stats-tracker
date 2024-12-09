import requests
import logging
import os
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
  
def get_competition_teams(id: str, year: int=2024) -> dict:
  try:
    allowed_ids = get_competitions_ids()
  except requests.exceptions.RequestException as e:
    logger.warning(f"failed to fetch competitions IDs ({str(e)})")
    raise e
  if not allowed_ids:
    logger.warning("got empty competitions IDs")
    raise UnknownIDError
  if id not in allowed_ids.keys():
    logger.warning(f"unknown id for competition teams lookup: {id}, allowed ids: {allowed_ids.keys()}")
    raise EmptyDataError
  uri = f'https://api.football-data.org/v4/competitions/{id}/teams?season={year}'
  headers = {'X-Auth-Token': API_KEY}
  response = requests.get(uri, headers=headers)
  response.raise_for_status() 
  teams = response.json().get('teams', {})
  return teams

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

def get_team_players(id: str) -> dict[str, str]:
  uri = f'https://api.football-data.org/v4/teams/{id}'
  headers = {'X-Auth-Token': API_KEY}
  try:
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.warning(f"failed to fetch teams' {id} players ({str(e)})")
    raise e
  result = {}
  for player in response.json().get('squad'):
    result[player["id"]] = player["name"]
  return result

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