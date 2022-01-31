from django.db import models

# Create your models here.

class User(models.Model):
    User_Id = models.CharField(max_length=200)
    User_Name = models.CharField(max_length=200)
    User_Password = models.CharField(max_length=200)
    User_Info = models.CharField(max_length=200)
    User_CreateDT = models.DateTimeField('date create')
    User_RecentDT = models.DateTimeField('date recent')