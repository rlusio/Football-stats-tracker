# Generated by Django 5.1.4 on 2024-12-05 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='joined_date',
            field=models.DateField(null=True),
        ),
    ]
