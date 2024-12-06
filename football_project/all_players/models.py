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
