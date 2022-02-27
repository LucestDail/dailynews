# Generated by Django 4.0.1 on 2022-02-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs4news', '0005_news_etc1_news_etc2_news_etc3_news_etc4_news_etc5'),
    ]

    operations = [
        migrations.CreateModel(
            name='News_Analysis_Count_Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_Analysis_Count_Company_Code', models.CharField(max_length=200)),
                ('News_Analysis_Count_Company_Count', models.CharField(max_length=200)),
                ('ETC1', models.TextField(blank=True)),
                ('ETC2', models.TextField(blank=True)),
                ('ETC3', models.TextField(blank=True)),
                ('ETC4', models.TextField(blank=True)),
                ('ETC5', models.TextField(blank=True)),
                ('News_Analysis_Count_Company_CreateDT', models.DateTimeField(verbose_name='date created')),
                ('News_Analysis_Count_Company_UpdateDT', models.DateTimeField(verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='News_Analysis_Word_Analysis_Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_Analysis_Word_Analysis_Company_Code', models.CharField(max_length=200)),
                ('News_Analysis_Word_Analysis_Company_Data', models.TextField(blank=True)),
                ('ETC1', models.TextField(blank=True)),
                ('ETC2', models.TextField(blank=True)),
                ('ETC3', models.TextField(blank=True)),
                ('ETC4', models.TextField(blank=True)),
                ('ETC5', models.TextField(blank=True)),
                ('News_Analysis_Word_Analysis_Company_CreateDT', models.DateTimeField(verbose_name='date created')),
                ('News_Analysis_Word_Analysis_Company_UpdateDT', models.DateTimeField(verbose_name='date updated')),
            ],
        ),
    ]