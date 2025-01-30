import unittest
from unittest.mock import patch, Mock
import scripts.api as api
import requests

class APITestCase(unittest.TestCase):
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
        result = api.get_competitions_ids()
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
        result = api.get_current_season("2014")
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
        result = api.get_competition_teams('2000', 2024)
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
        result = api.get_competition_standings("2000")
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
                },
                {
                    "id": 2,
                    "name": "Roberto Carlos",
                    "position": "Defence",
                    "dateOfBirth": "1987-02-19",
                    "nationality": "Brasil",
                    "shirtNumber": 3,
                }
            ]
        }
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response
        result = api.get_team_players("1234")
        expected_result = {
            1: {
                "name": "Daniel Krabus",
                "position": "Midfielder",
                "dateOfBirth": "1990-01-01",
                "nationality": "Ukraine",
                "shirtNumber": 10,
            },
            2: {
                "name": "Roberto Carlos",
                "position": "Defence",
                "dateOfBirth": "1987-02-19",
                "nationality": "Brasil",
                "shirtNumber": 3,
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
        result = api.get_player("1")
        expected_result = mock_response.json.return_value
        self.assertEqual(result, expected_result)

    @patch('scripts.api.requests.get')
    def test_get_players_matches(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'filters': {'limit': 15, 'offset': 0, 'competitions': 'FL1,CL,FL2', 'permission': 'TIER_ONE'},
            'resultSet': {'count': 0},
            'aggregations': 'As this a CPU intensive operation, this is only available for paid subscriptions.', 
            'person': {'id': 421,
                       'name': 'Mathieu Coutadeur', 
                       'firstName': 'Mathieu', 
                       'lastName': 'Coutadeur', 
                       'dateOfBirth': '1986-03-20', 
                       'nationality': 'France', 
                       'section': 'Midfield', 
                       'position': None, 'shirtNumber': 6, 
                       'lastUpdated': '2022-04-10T07:23:32Z'}, 
            'matches': []
            }
        mock_requests_get.return_value = mock_response
        result = api.get_players_matches("421")
        expected_result = mock_response.json.return_value
        self.assertEqual(result, expected_result)

    @patch('scripts.api.requests.get')
    def test_get_match_exception(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException("404 Client Error:  for url: https://api.football-data.org/v4/teams/64/matches/")
        with self.assertRaises(requests.exceptions.RequestException):
            api.get_match("64")

