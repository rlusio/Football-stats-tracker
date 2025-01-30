from django.core.management.base import BaseCommand
from all_players.models import Team, Player
import csv
import os

class Command(BaseCommand):
    help = "Import teams, coaches, and players from a single CSV file"

    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
        file_path = os.path.join(data_folder, 'competition_teams.csv')
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                team_id = row["team_id"]
                player_id = row["player_id"]
                team, created = Team.objects.get_or_create(
                    team_id=team_id,
                    defaults={
                        "season": row["season"],
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
                if not created:
                    updated_fields = {}
                    if not team.City and row.get("city"):
                        updated_fields["City"] = row["city"]
                    if not team.logo_url and row.get("crest_url"):
                        updated_fields["logo_url"] = row["crest_url"]
                    if not team.coach_name and row.get("coach_name"):
                        updated_fields["coach_name"] = row["coach_name"]
                    if not team.coach_nationality and row.get("coach_nationality"):
                        updated_fields["coach_nationality"] = row["coach_nationality"]
                    if not team.contract_start and row.get("contract_start"):
                        updated_fields["contract_start"] = row["contract_start"]
                    if not team.contract_end and row.get("contract_end"):
                        updated_fields["contract_end"] = row["contract_end"]
                    if updated_fields:
                        Team.objects.filter(team_id=team_id, season=row["season"]).update(**updated_fields)
                first_name, last_name = row["player_name"].split(" ", 1) if " " in row["player_name"] else (row["player_name"], "")
                player, created = Player.objects.get_or_create(
                    player_id=player_id,
                    defaults={
                        "firstname": first_name,
                        "lastname": last_name,
                        "position": row.get("position", "Unknown"),
                        "dateOfBirth": row.get("date_of_birth") or None,
                        "nationality": row.get("nationality", "Unknown"),
                        "team": team,   
                    }
                )
                if not created:
                    updated_fields = {}
                    if not player.position and row.get("position"):
                        updated_fields["position"] = row["position"]
                    if not player.dateOfBirth and row.get("date_of_birth"):
                        updated_fields["dateOfBirth"] = row["date_of_birth"]
                    if not player.nationality and row.get("nationality"):
                        updated_fields["nationality"] = row["nationality"]
                    if not player.team:
                        updated_fields["team"] = team   
                    if updated_fields:
                        Player.objects.filter(player_id=player_id).update(**updated_fields)
                self.stdout.write(self.style.SUCCESS(f"Processed team: {team.Team_Name} | Player: {first_name} {last_name}"))
        self.stdout.write(self.style.SUCCESS("Data import completed!"))
