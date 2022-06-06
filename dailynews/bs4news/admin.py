from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(News)
admin.site.register(News_Company)
admin.site.register(BS4_NEWS)
admin.site.register(BS4_NEWS_ANALYSIS)
admin.site.register(BS4_NEWS_COMPANY)
admin.site.register(BS4_NEWS_ANALYSIS_COUNT)
admin.site.register(BS4_NEWS_ANALYSIS_WORD)
admin.site.register(BS4_NEWS_COMPANY_CRAWL)
admin.site.register(BS4_NEWS_COMPANY_SCRAP)
admin.site.register(BS4_NEWS_ANALYSIS_WORD_EXCLUDED)