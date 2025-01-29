from django.test import TestCase
from all_players.models import Team, Player, Match
from django.db.utils import IntegrityError


class TeamModelTest(TestCase):
    def test_create_team_successfully(self):
        team = Team.objects.create(
            Team_Name="FC Barcelona",
            Country="Spain",
            City="Barcelona",
            marketValue=500000000,
            Number_of_Players=25,
            Standings=1
        )
        self.assertEqual(team.Team_Name, "FC Barcelona")
        self.assertEqual(team.marketValue, 500000000)
        
class PlayerModelTest(TestCase):
    def test_create_player_successfully(self):
        team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            marketValue=800000000,
            Number_of_Players=22,
            Standings=2
        )
        player = Player.objects.create(
            firstname="Karim",
            lastname="Benzema",
            nationality="France",
            marketValue=35000000,
            shirtNumber=9,
            team=team, 
        )
        self.assertEqual(player.firstname, "Karim")
        self.assertEqual(player.team, team)
        self.assertEqual(player.team.Team_Name, "Real Madrid")

    def test_create_player_missing_team(self):
        with self.assertRaises(IntegrityError):
            Player.objects.create(
                firstname="Karim",
                lastname="Benzema",
                nationality="France",
                marketValue=35000000,
                shirtNumber=9,
                team=None 
            )

    def test_create_player_with_default_values(self):
        team = Team.objects.create(
            Team_Name="Chelsea",
            Country="England",
            City="London",
            marketValue=700000000,
            Number_of_Players=23,
            Standings=3
        )
        player = Player.objects.create(
            firstname="N'Golo",
            lastname="Kanté",
            nationality="France",
            marketValue=80000000,
            shirtNumber=7,
            team=team, 
        )
        self.assertEqual(player.goals, 0)
        self.assertEqual(player.assists, 0)
        self.assertEqual(player.appearances, 0)


class MatchModelTest(TestCase):
    def test_create_match_successfully(self):
        team1 = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            marketValue=800000000,
            Number_of_Players=22,
            Standings=2
        )
        team2 = Team.objects.create(
            Team_Name="FC Barcelona",
            Country="Spain",
            City="Barcelona",
            marketValue=700000000,
            Number_of_Players=25,
            Standings=1
        )
        match = Match.objects.create(
            Competators=f"{team1.Team_Name} vs {team2.Team_Name}",
            Match_Place="Santiago Bernabéu",
            Competetion="La Liga",
            Season_Start_date="2024-08-01",
            Season_End_date="2025-05-31",
            Score="2-1",
            Status="Finished"
        )
        self.assertEqual(match.Competators, "Real Madrid vs FC Barcelona")
        self.assertEqual(match.Match_Place, "Santiago Bernabéu")
        self.assertEqual(match.Score, "2-1")
        self.assertEqual(match.Status, "Finished")
