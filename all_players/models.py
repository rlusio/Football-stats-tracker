from django.db import models

class Player(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=False)  
    joined_date = models.DateField(null=False)
    nationality = models.CharField(max_length=255, null=False)  
    marketValue = models.IntegerField(null=True)  
    shirtNumber=models.IntegerField(null=True)
    
class Team(models.Model):
    Team_Name = models.CharField(max_length=255, null=False)  
    Country = models.CharField(max_length=255, null=False) 
    City = models.CharField(max_length=255, null=False)  
    marketValue = models.IntegerField(null=True)  
    Number_of_Players = models.IntegerField(null=False)  
    Standings = models.IntegerField(null=False)  

class Match(models.Model):
    Competators = models.CharField(max_length=255, null=False)  
    Match_Place = models.CharField(max_length=255, null=False)  
    Competetion = models.CharField(max_length=255, null=False)  
    Season_Start_date = models.DateField(null=False)
    Season_End_date = models.DateField(null=False)  
    Score = models.CharField(max_length=255, null=False)
    Status = models.CharField(max_length=255, null=False)