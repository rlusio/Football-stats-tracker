from django.test import TestCase
from django.urls import reverse
from all_players.models import Player, Team, Match


class ViewTestsAllPlayers(TestCase):

    def setUp(self):
        # Tworzenie drużyny, gracza i meczu
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
        self.match = Match.objects.create(
            Competators="Real Madrid vs Barcelona",
            Match_Place="Santiago Bernabeu",
            Competetion="La Liga",
            Season_Start_date="2023-08-01",
            Season_End_date="2024-06-01",
            Score="3-1",
            Status="Finished"
        )
        # URL-e do testów
        self.home_url = reverse('home')
        self.all_players_url = reverse('all_players')
        self.team_players_url = reverse('team_players', kwargs={'team_id': self.team.id})
        self.all_matches_url = reverse('all_matches')
        self.all_teams_url = reverse('all_teams')
        self.details_url = reverse('details', kwargs={'id': self.player.id})
        self.team_details_url = reverse('team_details', kwargs={'id': self.team.id})
        self.match_details_url = reverse('match_details', kwargs={'id': self.match.id})
        self.top_market_value_url = reverse('top_market_value')
        self.top_performance_url = reverse('top_performance')
    def test_all_players_view(self):
        response = self.client.get(self.all_players_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cristiano Ronaldo")

    def test_team_players_view(self):
        response = self.client.get(self.team_players_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cristiano Ronaldo")

    def test_details_view(self):
        response = self.client.get(self.details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portugal")

    def test_all_teams_view(self):
        response = self.client.get(self.all_teams_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Madrid")

    def test_team_details_view(self):
        response = self.client.get(self.team_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spain")

    def test_all_matches_view(self):
        response = self.client.get(self.all_matches_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Madrid vs Barcelona")

    def test_match_details_view(self):
        response = self.client.get(self.match_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3-1")

    def test_top_market_value_view(self):
        Player.objects.all().delete()
        response = self.client.get(self.top_market_value_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Below $5M")
        self.assertContains(response, "$5M–$20M")
        self.assertContains(response, "Over $20M")

    def test_top_performance_view(self):
        Player.objects.all().delete()
        response = self.client.get(self.top_performance_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top Scorers (Goals > 10)")
        self.assertContains(response, "Top Assisters (Assists > 5)")