# Generated by Django 4.0.1 on 2022-01-31 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('News_from', models.CharField(max_length=200)),
                ('News_title', models.CharField(max_length=200)),
                ('News_company', models.CharField(max_length=200)),
                ('News_contents', models.TextField()),
                ('News_CreateDT', models.DateTimeField(verbose_name='date created')),
            ],
        ),
    ]
