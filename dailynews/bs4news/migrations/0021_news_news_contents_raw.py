# Generated by Django 4.0.1 on 2022-10-22 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs4news', '0020_bs4_news_company_crawl_result_execute_result_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='News_contents_raw',
            field=models.TextField(blank=True),
        ),
    ]