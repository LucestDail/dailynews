from django.contrib import admin
from .models import User, Noticeboard

# Register your models here.

admin.site.register(User)
admin.site.register(Noticeboard)