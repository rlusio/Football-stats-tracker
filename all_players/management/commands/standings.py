import csv
import os
from django.core.management.base import BaseCommand
from all_players.models import Team, Standing

class Command(BaseCommand):
    help = "Import season standings from CSV"

    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
        file_path = os.path.join(data_folder,'competition_standings.csv')
       
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                t = row.get('team_name')
                team, _ = Team.objects.update_or_create(
                    team_id=row["team_id"],
                    defaults={
                        "Team_Name": row["team_name"],
                        "short_name": row["short_name"],
                        "tla": row["tla"],
                        "logo_url": row["crest_url"],
                    }
                )
                Standing.objects.update_or_create(
                    season=row["season"],
                    team=team,
                    defaults={
                        "position": row["position"],
                        "played_games": row["played_games"],
                        "form": row["form"],
                        "won": row["won"],
                        "draw": row["draw"],
                        "lost": row["lost"],
                        "points": row["points"],
                        "goals_for": row["goals_for"],
                        "goals_against": row["goals_against"],
                        "goal_difference": row["goal_difference"],
                    }
                )
                self.stdout.write( self.style.SUCCESS(f"Processed {t}"))
        self.stdout.write(self.style.SUCCESS("✅ Standings imported successfully!"))
