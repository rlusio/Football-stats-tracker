from django.test import TestCase
from django.urls import reverse
from all_players.models import Player, Team, Match, Standing
from django.conf import settings
import os

class PlayerViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.player = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            team=self.team,
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000,
            shirtNumber=7,
            dateOfBirth="1985-02-05",
            goals=20,
            assists=10
        )
        self.details_url = reverse('details', kwargs={'id': self.player.id})
    
    def test_details_view(self):
        response = self.client.get(self.details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cristiano Ronaldo")
        self.assertContains(response, "Portugal")
        self.assertContains(response, 'player_plots')
class TeamPlayerViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.player = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            team=self.team,
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000,
            shirtNumber=7,
            dateOfBirth="1985-02-05",
            goals=20,
            assists=10
        )
        self.team_players_url = reverse('team_players', kwargs={'team_id': self.team.id})

    def test_team_players_view(self):
        response = self.client.get(self.team_players_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cristiano Ronaldo")
class AllPlayersViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.player1 = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            team=self.team,
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000,
            shirtNumber=7,
            dateOfBirth="1985-02-05",
            goals=20,
            assists=10
        )
        self.player2 = Player.objects.create(
            firstname="Karim",
            lastname="Benzema",
            position="Forward",
            team=self.team,
            joined_date="2014-08-01",
            nationality="France",
            marketValue=100000000,
            shirtNumber=9,
            dateOfBirth="1987-12-19",
            goals=15,
            assists=7
        )
        self.url = reverse('all_players')
    
    def test_all_players_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cristiano Ronaldo")
        self.assertContains(response, "Karim Benzema")
class ByPositionViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.player1 = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            team=self.team,
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000,
            shirtNumber=7,
            dateOfBirth="1985-02-05",
            goals=20,
            assists=10
        )
        self.url = reverse('by_position')
    
    def test_by_position_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forward")
class TeamDetailsViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.team_details_url = reverse('team_details', kwargs={'id': self.team.id})
    def test_team_details_view(self):
        response = self.client.get(self.team_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Madrid")
class AllTeamsViewTests(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        )
        self.team2 = Team.objects.create(
            Team_Name="Barcelona",
            Country="Spain",
            City="Barcelona",
            Number_of_Players=22,
            Standings=2,
            marketValue=2500000000
        )
        self.url = reverse('all_teams')
    
    def test_all_teams_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Madrid")
        self.assertContains(response, "Barcelona")
class MatchDetailsViewTests(TestCase):
    def setUp(self):
        self.match = Match.objects.create(
            Competators="Real Madrid vs Barcelona",
            Match_Place="Santiago Bernabeu",
            Competetion="La Liga",
            Season_Start_date="2023-08-01",
            Season_End_date="2024-06-01",
            Score="3-1",
            Status="Finished"
        )
        self.match_details_url = reverse('match_details', kwargs={'id': self.match.id})

    def test_match_details_view(self):
        response = self.client.get(self.match_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3-1") 
        self.assertContains(response, "Real Madrid vs Barcelona")  
class AllMatchesViewTests(TestCase):
    def setUp(self):
        self.match1 = Match.objects.create(
            Competators="Real Madrid vs Barcelona",
            Match_Place="Santiago Bernabeu",
            Competetion="La Liga",
            Season_Start_date="2023-08-01",
            Season_End_date="2024-06-01",
            Score="3-1",
            Status="Finished"
        )
        self.match2 = Match.objects.create(
            Competators="Atletico Madrid vs Sevilla",
            Match_Place="Wanda Metropolitano",
            Competetion="La Liga",
            Season_Start_date="2023-09-01",
            Season_End_date="2024-06-01",
            Score="2-2",
            Status="Finished"
        )
        self.url = reverse('all_matches')

    def test_all_matches_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Madrid vs Barcelona")
        self.assertContains(response, "Atletico Madrid vs Sevilla")