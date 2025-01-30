from django.test import TestCase
from all_players.models import Team, Player, Match, Competitions, Standing
from django.db.utils import IntegrityError
from datetime import date
from django.core.exceptions import ValidationError

class TeamModelTest(TestCase):
    def test_create_team_successfully(self):
        team = Team.objects.create(
            Team_Name="FC Barcelona",
            Country="Spain",
            City="Barcelona",
            marketValue=500000000,
            Number_of_Players=25,
            Standings=1,
            team_id=1
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
            Standings=2,
            team_id=2
        )
        player = Player.objects.create(
            firstname="Karim",
            lastname="Benzema",
            nationality="France",
            marketValue=35000000,
            shirtNumber=9,
            team=team,
            player_id=1
        )
        self.assertEqual(player.firstname, "Karim")
        self.assertEqual(player.team, team)
        self.assertEqual(player.team.Team_Name, "Real Madrid")

    def test_create_player_with_default_values(self):
        team = Team.objects.create(
            Team_Name="Chelsea",
            Country="England",
            City="London",
            marketValue=700000000,
            Number_of_Players=23,
            Standings=3,
            team_id=3
        )
        player = Player.objects.create(
            firstname="N'Golo",
            lastname="Kanté",
            nationality="France",
            marketValue=80000000,
            shirtNumber=7,
            team=team,
            player_id=3
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
            Standings=2,
            team_id=4
        )
        team2 = Team.objects.create(
            Team_Name="FC Barcelona",
            Country="Spain",
            City="Barcelona",
            marketValue=700000000,
            Number_of_Players=25,
            Standings=1,
            team_id=5
        )
        match = Match.objects.create(
            Competators=f"{team1.Team_Name} vs {team2.Team_Name}",
            Match_Place="Santiago Bernabéu",
            Competetion="La Liga",
            Season_Start_date=date(2024, 8, 1),
            Season_End_date=date(2025, 5, 31),
            Score="2-1",
            Status="Finished"
        )
        self.assertEqual(match.Competators, "Real Madrid vs FC Barcelona")
        self.assertEqual(match.Match_Place, "Santiago Bernabéu")
        self.assertEqual(match.Score, "2-1")
        self.assertEqual(match.Status, "Finished")
class StandingModelTest(TestCase):
    def test_create_standing_successfully(self):
        team = Team.objects.create(
            Team_Name="FC Barcelona",
            Country="Spain",
            City="Barcelona",
            marketValue=500000000,
            Number_of_Players=25,
            Standings=1
        )
        standing = Standing.objects.create(
            season=2024,
            position=1,
            team=team,
            played_games=38,
            form="WWDWL",
            won=24,
            draw=6,
            lost=8,
            points=78,
            goals_for=85,
            goals_against=40,
            goal_difference=45
        )
        self.assertEqual(standing.season, 2024)
        self.assertEqual(standing.position, 1)
        self.assertEqual(standing.team.Team_Name, "FC Barcelona")
        self.assertEqual(standing.points, 78)

    def test_create_standing_missing_required_fields(self):
        team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            marketValue=800000000,
            Number_of_Players=22,
            Standings=2
        )
        with self.assertRaises(IntegrityError):
            Standing.objects.create(
                season=2024,
                team=team 
            )

    def test_create_standing_missing_team(self):
        with self.assertRaises(IntegrityError):
            Standing.objects.create(
                season=2024,
                position=3,
                played_games=38,
                form="WWLWL",
                won=20,
                draw=10,
                lost=8,
                points=70,
                goals_for=75,
                goals_against=50,
                goal_difference=25
            )
            
    def test_create_standing_with_default_values(self):
        team = Team.objects.create(
            Team_Name="Juventus",
            Country="Italy",
            City="Turin",
            marketValue=600000000,
            Number_of_Players=23,
            Standings=4
        )
        standing = Standing.objects.create(
            season=2024,
            position=4,
            team=team,
            played_games=38
        )
        self.assertEqual(standing.form, "")
        self.assertEqual(standing.won, 0)
        self.assertEqual(standing.draw, 0)
        self.assertEqual(standing.lost, 0)
        self.assertEqual(standing.points, 0)
        self.assertEqual(standing.goals_for, 0)
        self.assertEqual(standing.goals_against, 0)
        self.assertEqual(standing.goal_difference, 0)