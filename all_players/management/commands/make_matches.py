from django.core.management.base import BaseCommand
from all_players.models import Match
from scripts.api import get_match
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch and save matches from Football-Data API"

    def handle(self, *args, **kwargs):
        competition_id = "2021"  # Premier League
        year = 2024  # Season year

        try:
            # Pobieranie meczów
            matches = get_match(competition_id, year)
            self.stdout.write(self.style.SUCCESS(f"Fetched {len(matches)} matches."))

            for match in matches:
                try:
                    # Przetwarzanie każdego meczu
                    home_team_name = match['homeTeam']['name']
                    away_team_name = match['awayTeam']['name']

                    Match.objects.update_or_create(
                        Competators=f"{home_team_name} vs {away_team_name}",
                        defaults={
                            'Match_Place': match.get('venue', 'Unknown'),
                            'Competetion': match['competition']['name'],
                            'Season_Start_date': match['season']['startDate'],
                            'Season_End_date': match['season']['endDate'],
                            'Score': f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}",
                            'Status': match['status'],
                        }
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Processed match: {home_team_name} vs {away_team_name}")
                    )
                    time.sleep(2)  # Przerwa między zapytaniami
                except Exception as e:
                    logger.warning(f"Failed to process match: {match.get('homeTeam', {}).get('name')} vs {match.get('awayTeam', {}).get('name')}: {e}")
                    self.stdout.write(self.style.WARNING(f"Failed to process match due to error."))

        except Exception as e:
            logger.error(f"Failed to fetch matches: {e}")
            self.stdout.write(self.style.ERROR(f"Error fetching matches: {e}"))
