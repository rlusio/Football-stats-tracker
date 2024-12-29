from django.urls import reverse, resolve
from django.test import TestCase
from all_players.views import all_players, details, all_matches, all_teams, match_details, team_details, viewed_items, user

class TestAllPlayersURLs(TestCase):
    def test_reverse_root_url(self):
        url = reverse('all_players')
        self.assertEqual(resolve(url).func, all_players)

    def test_reverse_all_players(self):
        url = reverse('all_players')
        self.assertEqual(resolve(url).func, all_players)

    def test_reverse_details(self):
        url = reverse('details', args=[1])
        self.assertEqual(resolve(url).func, details)

    def test_reverse_all_matches(self):
        url = reverse('all_matches')
        self.assertEqual(resolve(url).func, all_matches)

    def test_reverse_all_teams(self):
        url = reverse('all_teams')
        self.assertEqual(resolve(url).func, all_teams)

    def test_reverse_match_details(self):
        url = reverse('match_details', args=[1])
        self.assertEqual(resolve(url).func, match_details)

    def test_reverse_team_details(self):
        url = reverse('team_details', args=[1])
        self.assertEqual(resolve(url).func, team_details)

    def test_reverse_team_players(self):
        url = reverse('team_players', args=[1])  
        self.assertEqual(resolve(url).func, all_players)  

    def test_reverse_user(self):
        url = reverse('user')
        self.assertEqual(resolve(url).func, user) 

    def test_reverse_viewed_items(self):
        url = reverse('viewed_items')
        self.assertEqual(resolve(url).func, viewed_items)