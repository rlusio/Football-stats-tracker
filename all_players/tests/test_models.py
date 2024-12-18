from django.test import TestCase
from all_players.models import Player, Team, Match
from django.db import IntegrityError

class PlayerModelTest(TestCase):
    def test_create_player(self):
        player = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000
        )
        self.assertEqual(player.firstname, "Cristiano")
        self.assertEqual(player.lastname, "Ronaldo")
        self.assertEqual(player.position, "Forward")
        self.assertEqual(player.nationality, "Portugal")
        self.assertEqual(player.marketValue, 150000000)

    def test_missing__fields_player(self):
        try:
            player = Player.objects.create(
                firstname="Cristiano",
                lastname="Ronaldo",
                position="Forward",
                nationality="Portugal"
            )
            self.fail("IntegrityError not raised") 
        except IntegrityError:
            pass

class TeamModelTest(TestCase):
    
    def test_create_team(self):
        team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.assertEqual(team.Team_Name, "Real Madrid")
        self.assertEqual(team.Country, "Spain")
        self.assertEqual(team.City, "Madrid")
        self.assertEqual(team.Number_of_Players, 25)
        self.assertEqual(team.Standings, 1)
        self.assertEqual(team.marketValue, 3000000000)

    def test_missing_fields_team(self):
        try:
            team = Team.objects.create(
                Team_Name="Real Madrid",
                Country="Spain",
                City="Madrid",
                marketValue = 3000000000,
                Number_of_Players=25,
            )
            self.fail("IntegrityError not raised")
        except IntegrityError:
            pass

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
        self.assertEqual(match.Competators, "Real Madrid vs Barcelona")
        self.assertEqual(match.Match_Place, "Santiago Bernabeu")
        self.assertEqual(match.Competetion, "La Liga")
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
                Status = "Finished"
            )
            self.fail("IntegrityError not raised")
        except IntegrityError:
            pass