# Generated by Django 3.0.8 on 2021-07-27 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0019_session_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]