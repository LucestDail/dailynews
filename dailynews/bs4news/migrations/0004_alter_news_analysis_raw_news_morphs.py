# Generated by Django 4.0.1 on 2022-02-05 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs4news', '0003_alter_news_analysis_raw_etc1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news_analysis_raw',
            name='News_Morphs',
            field=models.TextField(blank=True),
        ),
    ]
