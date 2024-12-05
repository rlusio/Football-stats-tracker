#3. Zawodnicy, mecze pokryte w bazie danych i wypełnione przykładowymi danymi
import random


class Player:
    def __init__(self, name, age, team, nationality):
        self.name = name
        self.age = age
        self.team = team
        self.nationality = nationality
    def give_data_player(self):
        print("name:", self.name, "age:", self.age, "team:", self.team, "nationality:", self.nationality)

class Match:
    def __init__(self, result, teamA, teamB):
        self.result = result
        self.teamA = teamA
        self.teamB = teamB
    def give_data_match(self):
        print(self.teamA, "vs.", self.teamB, "final match result:", self.result)


if __name__ == "__main__":
    random_names = ("Kowalski", "Nowak", "Wisniewski", "Krawczyk")
    random_ages = range(18,35)
    random_teams = ["AGH_team", "UJ_team", "UEK_team", "UKEN_team"]
    random_nationality = ("pol", "ger", "uk", "rus")
    N=100
    players = []
    random_result = range(0,6)
    M=100
    games = []

    for i in range(N):
        name = random.choice(random_names)
        age = random.choice(random_ages)
        team = random.choice(random_teams)
        nationality = random.choice(random_nationality)
        players.append(Player(name, age, team, nationality))
        players[i].give_data_player()

    for i in range(M):
        result_teamA = random.choice(random_result)
        result_teamB = random.choice(random_result)
        result=[result_teamA,result_teamB]
        teamA = random.choice(random_teams)
        random_teams_2 = random_teams.copy()
        random_teams_2.remove(teamA)
        teamB = random.choice(random_teams_2)
        games.append(Match(result, teamA, teamB))
        games[i].give_data_match()
