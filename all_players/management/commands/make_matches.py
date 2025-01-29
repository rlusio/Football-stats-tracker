from django.core.management.base import BaseCommand
from all_players.models import Match
from scripts.api import get_match
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch and save matches from Football-Data API"

    def handle(self, *args, **kwargs):
        competition_id = "2021"  
        year = 2024   
        try:
            matches = get_match(competition_id, year)
            self.stdout.write(self.style.SUCCESS(f"Fetched {len(matches)} matches."))
            for match in matches:
                try:
                    home_team_name = match['homeTeam']['name']
                    away_team_name = match['awayTeam']['name']
                    referees = match.get('referees', [])
                    referee_details = ", ".join(
                        [f"Name: {ref.get('name', 'Unknown')}, Nationality: {ref.get('nationality', 'Unknown')}" for ref in referees]
                    )
                    Match.objects.update_or_create(
                        Competators=f"{home_team_name} vs {away_team_name}",
                        defaults={
                            'Match_Place': match.get('area', {}).get('name', 'Unknown'),
                            'Competetion': match.get('competition', {}).get('name', 'Unknown'),
                            'Match_Date': match.get('utcDate', None),
                            'Season_Start_date': match.get('season', {}).get('startDate', None),
                            'Season_End_date': match.get('season', {}).get('endDate', None),
                            'Score': f"{match.get('score', {}).get('fullTime', {}).get('home', 0)} - {match.get('score', {}).get('fullTime', {}).get('away', 0)}",
                            'Score_Details': f"{match.get('score', {}).get('halfTime', {}).get('home', 0)} - {match.get('score', {}).get('halfTime', {}).get('away', 0)}",
                            'Referees': referee_details,
                            'Status': match.get('status', 'Unknown'),
                            'Stage': match.get('stage', 'Unknown'),
                            'Last_Updated': match.get('lastUpdated', None),
                        }
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Processed match: {home_team_name} vs {away_team_name}")
                    )
                    time.sleep(2)   
                except Exception as e:
                    logger.warning(f"Failed to process match: {match.get('homeTeam', {}).get('name')} vs {match.get('awayTeam', {}).get('name')}: {e}")
                    self.stdout.write(self.style.WARNING(f"Failed to process match due to error."))
        except Exception as e:
            logger.error(f"Failed to fetch matches: {e}")
            self.stdout.write(self.style.ERROR(f"Error fetching matches: {e}"))
