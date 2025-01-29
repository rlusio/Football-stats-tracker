from django.db import models

class Team(models.Model):
    Team_Name = models.CharField(max_length=255, null=False)
    Country = models.CharField(max_length=255, null=False)
    City = models.CharField(max_length=255, null=False)
    marketValue = models.BigIntegerField(null=True)
    Number_of_Players = models.IntegerField(null=True)
    Standings = models.IntegerField(null=True)
    logo_url = models.URLField(null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    team_id = models.IntegerField(null=True, blank=True, unique=True)
    coach_name = models.CharField(max_length=255, null=True, blank=True)
    coach_nationality = models.CharField(max_length=255, null=True, blank=True)
    contract_start = models.CharField(max_length=10, null=True, blank=True)
    contract_end = models.CharField(max_length=10, null=True, blank=True)
    short_name = models.CharField(max_length=100, null=True, blank=True, default="")
    tla = models.CharField(max_length=10, null=True, blank=True, default="")
    def __str__(self):
        return f"{self.Team_Name} ({self.season})"


class Player(models.Model):
    player_id = models.IntegerField(unique=True,null=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=1)  
    joined_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=255)
    marketValue = models.BigIntegerField(null=True)
    shirtNumber = models.IntegerField(null=True)
    dateOfBirth = models.DateField(null=True, blank=True)  
    goals = models.IntegerField(default=0, null=True, blank=True)  
    assists = models.IntegerField(default=0, null=True, blank=True)  
    appearances = models.IntegerField(default=0, null=True, blank=True)  
        
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.team.Team_Name})"

    
class Match(models.Model):
    Competators = models.CharField(max_length=255, null=False) 
    Match_Date = models.DateTimeField(null=True, blank=True) 
    Match_Place = models.CharField(max_length=255, null=False)  
    Competetion = models.CharField(max_length=255, null=False)  
    Season_Start_date = models.DateField(null=False)
    Season_End_date = models.DateField(null=False)  
    Score = models.CharField(max_length=255, null=True)
    Score_Details = models.CharField(max_length=20, default="0 - 0")
    Status = models.CharField(max_length=255, null=False)
    Referees = models.TextField(null=True, blank=True)
    Stage = models.CharField(max_length=50, null=True, blank=True)
    Last_Updated = models.DateTimeField(null=True, blank=True) 
    def __str__(self):
        return f"{self.Competators} - {self.Match_Date}"

class Competitions(models.Model):
    Competitions = models.CharField(max_length=255, null=False)
   
class Standing(models.Model):
    season = models.IntegerField()  
    position = models.IntegerField()  
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="standings")
    played_games = models.IntegerField(default=0)
    form = models.CharField(max_length=20, null=True, blank=True, default="")  
    won = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team.Team_Name} - {self.season} (Position: {self.position})"

    