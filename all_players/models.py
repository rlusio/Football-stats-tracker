from django.db import models

class Team(models.Model):
    Team_Name = models.CharField(max_length=255, null=False)
    Country = models.CharField(max_length=255, null=False)
    City = models.CharField(max_length=255, null=False)
    marketValue = models.IntegerField(null=True)
    Number_of_Players = models.IntegerField(null=True)
    Standings = models.IntegerField(null=True)
    logo_url = models.URLField(null=True, blank=True)

class Player(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=1)  
    joined_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=255)
    marketValue = models.IntegerField(null=True)
    shirtNumber = models.IntegerField(null=True)
    dateOfBirth = models.DateField(null=True, blank=True)  
    goals = models.IntegerField(default=0, null=True, blank=True)  
    assists = models.IntegerField(default=0, null=True, blank=True)  
    appearances = models.IntegerField(default=0, null=True, blank=True)  
        
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.team.Team_Name})"

    
class Match(models.Model):
    Competators = models.CharField(max_length=255, null=False) 
    #Match_Date = models.DateTimeField(null=False)
    Match_Place = models.CharField(max_length=255, null=False)  
    Competetion = models.CharField(max_length=255, null=False)  
    Season_Start_date = models.DateField(null=False)
    Season_End_date = models.DateField(null=False)  
    Score = models.CharField(max_length=255, null=True)
    Status = models.CharField(max_length=255, null=False)
