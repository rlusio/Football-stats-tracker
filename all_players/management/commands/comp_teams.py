from django.core.management.base import BaseCommand
from all_players.models import Team, Player
import csv
import os

class Command(BaseCommand):
    help = "Import teams, coaches, and players from a single CSV file"
    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
        file_path = os.path.join(data_folder,'competition_teams.csv')
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                t = row.get('team_name')
                team, created = Team.objects.update_or_create(
                    team_id=row["team_id"],
                    season=row["season"],
                    defaults={
                        "Team_Name": row["team_name"],
                        "Country": row["country"],
                        "City": row.get("city", "Unknown"),
                        "logo_url": row.get("crest_url", ""),
                        "coach_name": row.get("coach_name"),
                        "coach_nationality": row.get("coach_nationality"),
                        "contract_start": row.get("contract_start"),
                        "contract_end": row.get("contract_end"),
                    }
                )
                first_name, last_name = row["player_name"].split(" ", 1) if " " in row["player_name"] else (row["player_name"], "")
                Player.objects.update_or_create(
                    player_id=row["player_id"],
                    team=team,
                    defaults={
                        "firstname": first_name,
                        "lastname": last_name,
                        "position": row.get("position", "Unknown"),
                        "dateOfBirth": row.get("date_of_birth") or None,
                        "nationality": row.get("nationality", "Unknown"),
                    }
                )
                self.stdout.write( self.style.SUCCESS(f"Processed {t}"))
        self.stdout.write(self.style.SUCCESS(" Data import completed!"))
