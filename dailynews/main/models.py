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
    USER_ETC01 = models.CharField(max_length=200, blank=True)
    USER_ETC02 = models.CharField(max_length=200, blank=True)
    USER_ETC03 = models.CharField(max_length=200, blank=True)
    USER_ETC04 = models.CharField(max_length=200, blank=True)
    USER_ETC05 = models.CharField(max_length=200, blank=True)


class Dashboard(models.Model):
    Dashboard_Total_News_Count = models.CharField(max_length=200)
    Dashboard_Total_Analysis_Count = models.CharField(max_length=200)
    Dashboard_Total_Analysis_Rate = models.CharField(max_length=200)
    Dashboard_Today_count = models.CharField(max_length=200)
    Dashboard_CreateDT = models.DateTimeField('date create')
    Dashboard_ETC01 = models.CharField(max_length=200, blank=True)
    Dashboard_ETC02 = models.CharField(max_length=200, blank=True)
    Dashboard_ETC03 = models.CharField(max_length=200, blank=True)
    Dashboard_ETC04 = models.CharField(max_length=200, blank=True)
    Dashboard_ETC05 = models.CharField(max_length=200, blank=True)


class Noticeboard(models.Model):
    Noticeboard_Type = models.CharField(max_length=200)
    Noticeboard_Title = models.CharField(max_length=200)
    Noticeboard_Content = models.TextField(blank=True)
    Noticeboard_Type = models.CharField(max_length=200)
    Noticeboard_CreateDT = models.DateTimeField('date create')
    Noticeboard_UpdateDT = models.DateTimeField('date recent')
    Noticeboard_ETC01 = models.CharField(max_length=200, blank=True)
    Noticeboard_ETC02 = models.CharField(max_length=200, blank=True)
    Noticeboard_ETC03 = models.CharField(max_length=200, blank=True)
    Noticeboard_ETC04 = models.CharField(max_length=200, blank=True)
    Noticeboard_ETC05 = models.CharField(max_length=200, blank=True)