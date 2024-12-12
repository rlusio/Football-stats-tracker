from django.db import models

class Player(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    position = models.CharField(max_length=255,null=True)
    joined_date=models.DateField(null=True)
    nationality=models.CharField(max_length=255, null=True)
    shirtNumber=models.IntegerField(null=True)
    marketValue=models.IntegerField(null=True)
    # Create your models here.
class Team(models.Model):
    Team_Name = models.CharField(max_length=255,null=True)
    Country = models.CharField(max_length=255,null=True)
    City =models.CharField(max_length=255 ,null=True)
    marketValue=models.IntegerField(null=True)
    Number_of_Players = models.IntegerField(null=True)
    Standings= models.IntegerField(null=True)

class Match(models.Model):
    Competators = models.CharField(max_length=255,null=True)
    Match_Place = models.CharField(max_length=255,null=True)
    Competetion = models.CharField(max_length=255 , null=True)
    Season_Start_date =models.DateField(null=True)
    Season_End_date =models.DateField(null=True)
    Score = models.CharField(max_length=255 ,null=True)
    Status = models.CharField(max_length=255, null=True)
