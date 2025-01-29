from django.core.management.base import BaseCommand
from all_players.models import Match
import logging
import csv
import os


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch and save matches from Football-Data API"

    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
        file_path = os.path.join(data_folder,'formatted_matches.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
            return
        try:
            with open(file_path,'r',encoding='utf-8') as file:
                reader = csv.DictReader(file)  
                match_count = 0
                for row in reader:
                    try:
                        home_team = row.get('homeTeam', 'Unknown')
                        away_team = row.get('awayTeam', 'Unknown')
                        competition = row.get('competition', 'Unknown')
                        match_date = row.get('matchDate', None)
                        season_start = row.get('seasonStart', '2000-01-01')
                        season_end = row.get('seasonEnd', '2000-12-31')
                        full_time_score = row.get('fullTimeScore', '0 - 0')
                        half_time_score = row.get('halfTimeScore', '0 - 0')
                        referees = row.get('referees', 'Unknown')
                        status = row.get('status', 'Unknown')
                        stage = row.get('stage', 'Unknown')
                        last_updated = row.get('lastUpdated', None)
                        Match.objects.update_or_create(
                            Competators=f"{home_team} vs {away_team}",
                            defaults={
                                'Match_Place': "Unknown",
                                'Competetion': competition,
                                'Match_Date': match_date,
                                'Season_Start_date': season_start,
                                'Season_End_date': season_end,
                                'Score': full_time_score,
                                'Score_Details': half_time_score,
                                'Referees': referees,
                                'Status': status,
                                'Stage': stage,
                                'Last_Updated': last_updated,
                            }    
                        )
                        match_count+= 1
                        self.stdout.write( self.style.SUCCESS(f"Processed match: {home_team} vs {away_team}"))
                    except Exception as e:
                        logger.warning(f" Failed to process match: {home_team} vs {away_team} → {e}")
                        self.stdout.write(self.style.WARNING(f" Failed to process match due to error."))  
            self.stdout.write(self.style.SUCCESS(f" Successfully processed {match_count} matches!"))                
        except Exception as e:
            logger.error(f"Failed to load matches from file: {e}")
            self.stdout.write(self.style.ERROR(f"Error loading matches: {e}"))


        