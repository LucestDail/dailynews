# Generated by Django 4.0.1 on 2022-02-27 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_noticeboard_noticeboard_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='User_Focus_Company_1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='User_Focus_Company_2',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]