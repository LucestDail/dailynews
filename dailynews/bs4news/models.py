from django.db import models

# Create your models here.

class News(models.Model):
    News_from = models.CharField(db_index=True, max_length=200)
    News_title = models.CharField(db_index=True, max_length=200)
    News_company = models.CharField(db_index=True, max_length=200)
    News_contents = models.TextField()
    News_CreateDT = models.DateTimeField('date created')
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class News_Company(models.Model):
    News_Company_Code = models.CharField(max_length=200)
    News_Company_Name = models.CharField(max_length=200)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)
    News_Company_CreateDT = models.DateTimeField('date created')
    News_Company_UpdateDT = models.DateTimeField('date updated')


class News_Analysis_Raw(models.Model):
    News_Analysis_Company = models.CharField(db_index=True, max_length=200)
    News_Analysis_Title = models.CharField(db_index=True, max_length=200)
    News_Analysis_From = models.CharField(db_index=True, max_length=200)
    News_Morphs = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)
    News_Analysis_CreateDT = models.DateTimeField('date created')