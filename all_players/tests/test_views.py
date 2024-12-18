from django.test import TestCase
from django.urls import reverse
from all_players.models import Player, Team, Match

class ViewTestsAllPlayers(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.all_players_url = reverse('all_players')
        self.all_matches_url = reverse('all_matches')
        self.all_teams_url = reverse('all_teams')
        self.details_url = reverse('details', kwargs={'id': 1})
        self.player = Player.objects.create(
            firstname="Cristiano",
            lastname="Ronaldo",
            position="Forward",
            joined_date="2009-06-01",
            nationality="Portugal",
            marketValue=150000000,
            shirtNumber=7
        )
        self.team = Team.objects.create(
            Team_Name="Real Madrid",
            Country="Spain",
            City="Madrid",
            Number_of_Players=25,
            Standings=1,
            marketValue=3000000000
        ) 
        self.match = Match.objects.create(
            Competators="Real Madrid vs Barcelona",
            Match_Place="Santiago Bernabeu",
            Competetion="La Liga",
            Season_Start_date="2023-08-01",
            Season_End_date="2023-06-01",
            Score="3-1",
            Status="Finished"
        )

    def test_main_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Football Stats Tracker")
