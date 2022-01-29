from django.db import models

# Create your models here.

class News(models.Model):
    News_from = models.CharField(max_length=200)
    News_title = models.CharField(max_length=200)
    News_contents = models.TextField()
    News_CreateDT = models.DateTimeField('date created')