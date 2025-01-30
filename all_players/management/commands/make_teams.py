from django.core.management.base import BaseCommand
from all_players.models import Team, Player
from scripts.api import get_competition_teams, get_team_players
import time
import logging

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = "Make the database with teams and players from Football-Data API"
    def handle(self, *args, **kwargs):
        competition_id = "2021"  
        year = 2024  
        try:
            teams = get_competition_teams(competition_id, year)
            for team in teams:
                db_team, created = Team.objects.update_or_create(
                    Team_Name=team['name'],
                    defaults={
                        'Country': team['area']['name'],
                        'City': team.get('venue', 'Unknown'),
                        'logo_url': team.get('crest'),
                    }
                )
                self.stdout.write(
                    self.style.SUCCESS(f"{'Created' if created else 'Updated'} team: {db_team.Team_Name}")
                )
                try:
                    players = get_team_players(team['id'])
                    for player_id, player_info in players.items():
                        Player.objects.update_or_create(
                            firstname=player_info["name"].split()[0],
                            lastname=" ".join(player_info["name"].split()[1:]),
                            team=db_team,
                            defaults={
                                'position': player_info.get("position", "Unknown"),
                                'dateOfBirth': player_info.get("dateOfBirth"),
                                'nationality': player_info.get("nationality", "Unknown"),
                                'shirtNumber': player_info.get("shirtNumber"),
                                'marketValue': player_info.get("marketValue",None),  
                                'goals': player_info.get("goals", 0),  
                                'assists': player_info.get("assists", 0),  
                                'appearances': player_info.get("appearances", 0),                              }
                        )
                    db_team.Number_of_Players = len(players)
                    db_team.save()
                except Exception as e:
                    logger.warning(f"Failed to process players for team {team['name']} (ID: {team['id']}): {e}")
                    self.stdout.write(
                        self.style.WARNING(f"Failed to process players for team {team['name']} due to error.")
                    )
                time.sleep(4)
        except Exception as e:
            logger.error(f"Failed to fetch teams: {e}")
            self.stdout.write(self.style.ERROR(f"Error fetching teams: {e}"))
