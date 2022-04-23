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


class News_Analysis_Count_Company(models.Model):
    News_Analysis_Count_Company_Code = models.CharField(max_length=200)
    News_Analysis_Count_Company_Count = models.CharField(max_length=200)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)
    News_Analysis_Count_Company_CreateDT = models.DateTimeField('date created')
    News_Analysis_Count_Company_UpdateDT = models.DateTimeField('date updated')


class News_Analysis_Word_Analysis_Company(models.Model):
    News_Analysis_Word_Analysis_Company_Code = models.CharField(max_length=200)
    News_Analysis_Word_Analysis_Company_Data = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)
    News_Analysis_Word_Analysis_Company_CreateDT = models.DateTimeField('date created')
    News_Analysis_Word_Analysis_Company_UpdateDT = models.DateTimeField('date updated')


class BS4_NEWS_COMPANY(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    COMPANY_NAME = models.CharField(max_length=200)
    DOMAIN_URL = models.TextField(blank=True)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS_COMPANY_CRAWL(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    DOMAIN_URL = models.TextField(blank=True)
    DOMAIN_QUERY_STRING = models.TextField(blank=True)
    CRAWL_TYPE = models.TextField(blank=True)
    CRAWL_LINK_TARGET = models.TextField(blank=True)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    TYPE_TOOLS1 = models.TextField(blank=True)
    TYPE_TOOLS2 = models.TextField(blank=True)
    TYPE_TOOLS3 = models.TextField(blank=True)
    TYPE_TOOLS4 = models.TextField(blank=True)
    TYPE_TOOLS5 = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS_COMPANY_SCRAP(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    DOMAIN_URL = models.TextField(blank=True)
    DOMAIN_QUERY_STRING = models.TextField(blank=True)
    SCRAP_TYPE = models.TextField(blank=True)
    TITLE_TAG = models.TextField(blank=True)
    TITLE_XPATH = models.TextField(blank=True)
    AUTHOR_TAG = models.TextField(blank=True)
    AUTHOR_XPATH = models.TextField(blank=True)
    CONTENTS_TAG = models.TextField(blank=True)
    CONTENTS_XPATH = models.TextField(blank=True)
    DATE_TAG = models.TextField(blank=True)
    DATE_XPATH = models.TextField(blank=True)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    NEWS_AUTHOR = models.CharField(db_index=True, max_length=200)
    MEWS_TITLE = models.CharField(db_index=True, max_length=200)
    NEWS_CONTENTS = models.TextField(blank=True)
    NEWS_URL = models.TextField(blank=True)
    NEWS_DATE = models.CharField(db_index=True, max_length=200)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS_ANALYSIS(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    NEWS_AUTHOR = models.CharField(db_index=True, max_length=200)
    MEWS_TITLE = models.CharField(db_index=True, max_length=200)
    NEWS_MORPHS = models.TextField(blank=True)
    NEWS_DATE = models.CharField(db_index=True, max_length=200)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS_ANALYSIS_COUNT(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    NEWS_COUNT = models.TextField(blank=True)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS_ANALYSIS_WORD(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    NEWS_ANALYSIS_WORD = models.TextField(blank=True)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    DESCRIPTION_INFO = models.TextField(blank=True)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)


class BS4_NEWS_ANALYSIS_WORD_EXCLUDED(models.Model):
    COMPANY_CODE = models.CharField(db_index=True, max_length=200)
    EXCLUDED_WORD = models.TextField(blank=True)
    DESCRIPTION_INFO = models.TextField(blank=True)
    UPDATE_DATETIME = models.DateTimeField('date updated')
    UPDATE_USER = models.CharField(db_index=True, max_length=200)
    CREATE_DATETIME = models.DateTimeField('date created')
    CREATE_USER = models.CharField(db_index=True, max_length=200)
    ETC1 = models.TextField(blank=True)
    ETC2 = models.TextField(blank=True)
    ETC3 = models.TextField(blank=True)
    ETC4 = models.TextField(blank=True)
    ETC5 = models.TextField(blank=True)