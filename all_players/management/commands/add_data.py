from django.core.management.base import BaseCommand
from all_players.models import Player, Team, Match
from datetime import date

class Command(BaseCommand):
    help = 'Add initial data to the database'

    def handle(self, *args, **kwargs):
        # Dodanie graczy
        Player.objects.create(
            firstname="Lionel",
            lastname="Messi",
            position="Forward",
            joined_date=date(2004, 11, 16),
            nationality="Argentina",
            marketValue=50000000,
            shirtNumber=10
        )
        Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            joined_date=date(2003, 8, 16),
            nationality="Portugal",
            marketValue=60000000,
            shirtNumber=7
        )

        # Dodanie drużyn
        Team.objects.create(
            Team_Name="FC Barcelona",
            Country="Spain",
            City="Barcelona",
            marketValue=800000000,
            Number_of_Players=25,
            Standings=1
        )
        Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            marketValue=850000000,
            Number_of_Players=24,
            Standings=2
        )

        # Dodanie meczu
        Match.objects.create(
            Competators="FC Bar ",
            Match_Place="Camp Nou",
            Competetion="La Liga",
            Season_Start_date=date(2023, 8, 12),
            Season_End_date=date(2024, 5, 19),
            Score="2-1",
            Status="Finished"
        )
        Match.objects.create(
            Competators="FC  Madrid",
            Match_Place="Camp Nou",
            Competetion="La Liga",
            Season_Start_date=date(2023, 8, 12),
            Season_End_date=date(2024, 5, 19),
            Score="2-1",
            Status="Finished"
        )

        self.stdout.write(self.style.SUCCESS('Successfully added initial data!'))
