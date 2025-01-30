import csv
import os
from django.core.management.base import BaseCommand
from all_players.models import Team, Player, Match

class Command(BaseCommand):
    help = "Import players and matches from CSV, ensuring correct linking of multiple matches per player"

    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
        players_file = os.path.join(data_folder, 'playersData.csv')
        matches_file = os.path.join(data_folder, 'matchesData.csv')

        matches_dict = {}
        with open(matches_file, newline='', encoding="utf-8") as matches_csv:
            matches_reader = csv.DictReader(matches_csv)
            for match_row in matches_reader:
                player_id = match_row["id"]
                if player_id not in matches_dict:
                    matches_dict[player_id] = []
                matches_dict[player_id].append(match_row)

        with open(players_file, newline='', encoding="utf-8") as players_csv:
            players_reader = csv.DictReader(players_csv)

            for player_row in players_reader:
                try:
                    name_parts = player_row["name"].split(" ", 1)
                    firstname = name_parts[0]
                    lastname = name_parts[1] if len(name_parts) > 1 else ""

                    player, created = Player.objects.update_or_create(
                        player_id=player_row["id"],
                        defaults={
                            "firstname": firstname,
                            "lastname": lastname,
                            "dateOfBirth": player_row.get("date_of_birth") or None,
                            "nationality": player_row.get("nationality", "Unknown"),
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"New player added: {player.firstname} {player.lastname}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Player updated: {player.firstname} {player.lastname}"))

                    player_matches = matches_dict.get(player_row["id"], [])
                    for match_row in player_matches:
                        competitors = f"{match_row['home_team']} vs {match_row['away_team']}"
                        score = f"{match_row.get('final_home', '0')} - {match_row.get('final_away', '0')}"

                        match, created = Match.objects.update_or_create(
                            Competators=competitors,
                            player=player,  
                            defaults={
                                "winner": match_row["winner"],
                                "duration": match_row["duration"],
                                "Score": score,
                            }
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f"New match added: {competitors} | Score: {score}"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Match updated: {competitors} | Score: {score}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing player/match row: {player_row} - {e}"))

        self.stdout.write(self.style.SUCCESS("Data import completed."))
