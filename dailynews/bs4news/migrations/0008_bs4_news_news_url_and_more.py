# Generated by Django 4.0.1 on 2022-04-23 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs4news', '0007_bs4_news_bs4_news_analysis_bs4_news_analysis_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bs4_news',
            name='NEWS_URL',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='bs4_news_company_scrap',
            name='DOMAIN_QUERY_STRING',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='bs4_news_company_scrap',
            name='DOMAIN_URL',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='bs4_news',
            name='NEWS_CONTENTS',
            field=models.TextField(blank=True),
        ),
    ]