from django.test import TestCase
from all_players.models import Player, Team, Match
from django.db import IntegrityError
from datetime import date

class PlayerModelTest(TestCase):
    
    def setUp(self):
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            marketValue=3000000000,
            Number_of_Players=25,
            Standings=1,
        )

    def test_create_player(self):
        player = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            team=self.team,
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000,
            shirtNumber=7,
            dateOfBirth="1985-02-05"
        )
        self.assertEqual(player.firstname, "Cristiano")
        self.assertEqual(player.lastname, "Ronaldo")
        self.assertEqual(player.position, "Forward")
        self.assertEqual(player.nationality, "Portugal")
        self.assertEqual(player.marketValue, 150000000)
        self.assertEqual(player.shirtNumber, 7)
        self.assertEqual(player.dateOfBirth, "1985-02-05")
        self.assertEqual(player.team.Team_Name, "Real Madrid")
        
class TeamModelTest(TestCase):
    
    def test_create_team(self):
        team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            marketValue=3000000000,
            Number_of_Players=25,
            Standings=1,
        )
        self.assertEqual(team.Team_Name, "Real Madrid")
        self.assertEqual(team.Country, "Spain")
        self.assertEqual(team.City, "Madrid")
        self.assertEqual(team.Number_of_Players, 25)
        self.assertEqual(team.Standings, 1)
        self.assertEqual(team.marketValue, 3000000000)

class MatchModelTest(TestCase):
    
    def test_create_match(self):
        match = Match.objects.create(
            Competators="Real Madrid vs Barcelona",
            Match_Place="Santiago Bernabeu",
            Competetion="La Liga",
            Season_Start_date="2023-08-01",
            Season_End_date="2023-06-01",
            Score="3-1",
            Status="Finished"
        )
        self.assertEqual(match.Season_Start_date, "2023-08-01")
        self.assertEqual(match.Season_End_date, "2023-06-01")
        self.assertEqual(match.Score, "3-1")
        self.assertEqual(match.Status, "Finished")

    def test_missing_fields_match(self):
        try:
            match = Match.objects.create(
                Competators="Real Madrid vs Barcelona",
                Match_Place="Santiago Bernabeu",
                Competetion="La Liga",
                Season_End_date="2023-06-01",
                Score="3-1",
                Status="Finished"
            )
            self.fail("IntegrityError not raised")
        except IntegrityError:
            pass