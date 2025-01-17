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

def get_players_matches(id: str):
  uri = f'https://api.football-data.org/v4/persons/{id}/matches'
  headers = {'X-Auth-Token': API_KEY} 
  try:
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.warning(f"failed to fetch players' {id} data ({str(e)})")
    raise e
  return response.json()
  
def get_player_stats(id: str):
    data = get_players_matches(id)
    stats = []
    player_info = {
        "player": {
            "name": data["person"]["name"],
            "date_of_birth": data["person"]["dateOfBirth"],
            "position": data["person"]["position"],
            "nationality": data["person"]["nationality"],
        }}
    stats.append(player_info)
    for match in data["matches"]:
        season = {
            "start_date": match["season"]["startDate"],
            "end_date": match["season"]["endDate"],
        }
        match_results = {
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "winner": match.get("season", {}).get("winner", {}).get("name", "No winner") if match.get("season", {}).get("winner") else "No winner",
            "duration": match["score"]["duration"],
            "half_time_result": match["score"]["halfTime"],
            "final_result": match["score"]["fullTime"],
            "extra_time_result": match["score"].get("extraTime", None),
            "penalties_result": match["score"].get("penalties", None),
        }
        stats.append(season)
        stats.append(match_results)
    return stats
    

def get_match(competition_id, year: int = 2024):
  uri = f'https://api.football-data.org/v4/teams/{competition_id}/matches/'
  headers = {'X-Auth-Token': API_KEY}
  try:
    response = requests.get(uri, headers=headers )
    response.raise_for_status()
    if response.headers.get("Content-Type", "").startswith("application/json"):
      matches = response.json().get("matches", [])
      return matches
    else:
      logger.error(f"Unexpected response format: {response.text}")
      raise ValueError("Response is not JSON")

  except requests.exceptions.RequestException as e:
    logger.warning(f"failed to fetch matches' {id} data ({str(e)})")
    raise e

def get_particular_match(match_id):
  uri = f'https://api.football-data.org/v4/matches/{match_id}'
  headers = {'X-Auth-Token': API_KEY}
  try:
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.warning(f"Failed to fetch match details: {response.status_code} {response.text}")
    raise e
  return response.json()
def get_match_stats(competition_id: str, year: int = 2024) -> list:
  matches = get_match(competition_id, year)
  stats = []
  for match in matches:
      match_stats = get_particular_match(match["id"])
      match_data = {
          "home_team": match["homeTeam"]["name"],
          "away_team": match["awayTeam"]["name"],
          "date": match["utcDate"],
          "half_time_score": match["score"]["halfTime"],
          "score": match["score"]["fullTime"],
          "half_time_score": match["score"]["halfTime"],
          "extra_time_result": match["score"].get("extraTime", None),
          "penalties_result": match["score"].get("penalties", None),


      }
      goal_details = []
      for goal in match_stats.get("goals", []):
          goal_details.append({
              "minute": goal["minute"],
              "type": goal["type"],
              "scorer": goal["scorer"]["name"],
              "team" : goal["team"]["name"],
              "assist": goal.get("assist", {}).get("name"),
          })
      match_data["goal_details"] = goal_details
      match_data["home_team_statistics"] = match_stats.get("homeTeam", {}).get("statistics", {})
      match_data["away_team_statistics"] = match_stats.get("awayTeam", {}).get("statistics", {})
      stats.append(match_data)
  return stats  
