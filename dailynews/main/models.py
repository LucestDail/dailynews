from django.db import models

# Create your models here.

class User(models.Model):
    User_Id = models.CharField(max_length=200)
    User_Name = models.CharField(max_length=200)
    User_Password = models.CharField(max_length=200)
    User_Info = models.CharField(max_length=200)
    User_CreateDT = models.DateTimeField('date create')
    User_RecentDT = models.DateTimeField('date recent')
    User_MobileNumber = models.CharField(max_length=200, blank=True)
    User_Email = models.CharField(max_length=200, blank=True)
    User_Focus_word = models.CharField(max_length=200, blank=True)
    User_Focus_Company = models.CharField(max_length=200, blank=True)


class Dashboard(models.Model):
    Dashboard_Total_News_Count = models.CharField(max_length=200)
    Dashboard_Total_Analysis_Count = models.CharField(max_length=200)
    Dashboard_Total_Analysis_Rate = models.CharField(max_length=200)
    Dashboard_Today_count = models.CharField(max_length=200)
    Dashboard_CreateDT = models.DateTimeField('date create')