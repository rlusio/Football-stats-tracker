import unittest
from unittest.mock import patch, Mock
from django.test import TestCase
from scripts.api import *

class APITestCase(TestCase):
    @patch('scripts.api.requests.get')
    def test_get_competitions_ids(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'competitions': [
                {'id': '2000', 'name': 'Premier League'},
                {'id': '2001', 'name': 'La Liga'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        result = get_competitions_ids()
        expected_result = {
            '2000': 'Premier League',
            '2001': 'La Liga'
        }
        self.assertEqual(result, expected_result)

    @patch('scripts.api.requests.get')
    @patch('scripts.api.get_competitions_ids')
    def test_get_current_season(self, mock_get_competitions_ids, mock_requests_get):
        mock_get_competitions_ids.return_value = {"2014": "aaaa"}
        mock_response = Mock()
        mock_response.json.return_value = {
            "currentSeason": {
                "id": 2292,
                "startDate": "2024-08-18",
                "endDate": "2025-05-25",
                "currentMatchday": 20,
                "winner": None
            }
        }
        mock_requests_get.return_value = mock_response
        result = get_current_season("2014")
        expected_result = {
            "id": 2292,
            "startDate": "2024-08-18",
            "endDate": "2025-05-25",
            "currentMatchday": 20,
            "winner": None
        }
        self.assertEqual(result, expected_result)
    
    @patch('scripts.api.requests.get')
    def test_get_competition_teams(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'teams': [
                {'id': '1', 'name': 'Real Madrid'},
                {'id': '2', 'name': 'Lech Poznan'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        result = get_competition_teams('2000', 2024)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Real Madrid')

    @patch('scripts.api.requests.get')
    @patch('scripts.api.get_competitions_ids')
    def test_get_competition_standings(self, mock_get_competitions_ids, mock_requests_get):
        mock_get_competitions_ids.return_value = {"2000": "Premier League"}
        mock_response = Mock()
        mock_response.json.return_value = {
            "standings": [
                {"type": "TOTAL", "table": [{"team": {"id": 1, "name": "Team A"}}]}
            ]
        }
        mock_requests_get.return_value = mock_response
        result = get_competition_standings("2000")
        expected_result = [{"team": {"id": 1, "name": "Team A"}}]
        self.assertEqual(result, expected_result)

    @patch('scripts.api.requests.get')
    def test_get_team_players(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "squad": [
                {
                    "id": 1,
                    "name": "Daniel Krabus",
                    "position": "Midfielder",
                    "dateOfBirth": "1990-01-01",
                    "nationality": "Ukraine",
                    "shirtNumber": 10,
                    'marketValue': 10, 
                    'goals': 0,
                    'assists': 1,
                    'appearances': 22,
                },
                {
                    "id": 2,
                    "name": "Roberto Carlos",
                    "position": "Defence",
                    "dateOfBirth": "1987-02-19",
                    "nationality": "Brasil",
                    "shirtNumber": 3,
                    'marketValue': 10000000, 
                    'goals': 14,
                    'assists': 2,
                    'appearances': 25,
                }
            ]
        }
        mock_requests_get.return_value = mock_response
        result = get_team_players("1234")
        expected_result = {
            1: {
                "name": "Daniel Krabus",
                "position": "Midfielder",
                "dateOfBirth": "1990-01-01",
                "nationality": "Ukraine",
                "shirtNumber": 10,
                'marketValue': 10, 
                'goals': 0,
                'assists': 1,
                'appearances': 22,
            },
            2: {
                "name": "Roberto Carlos",
                "position": "Defence",
                "dateOfBirth": "1987-02-19",
                "nationality": "Brasil",
                "shirtNumber": 3,
                'marketValue': 10000000, 
                'goals': 14,
                'assists': 2,
                'appearances': 25,
            }
        }
        self.assertEqual(result, expected_result)

    @patch('scripts.api.requests.get')
    def test_get_player(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "Daniel Krabus",
            "position": "Midfielder",
            "dateOfBirth": "1990-01-01",
            "nationality": "Ukraine",
            "shirtNumber": 10
        }
        mock_requests_get.return_value = mock_response
        result = get_player("1")
        expected_result = mock_response.json.return_value
        self.assertEqual(result, expected_result)
