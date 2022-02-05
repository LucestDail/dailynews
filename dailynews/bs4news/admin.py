from django.contrib import admin
from .models import News, News_Company

# Register your models here.

admin.site.register(News)
admin.site.register(News_Company)