# Generated by Django 3.0.8 on 2021-07-18 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0015_auto_20210715_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='level',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
