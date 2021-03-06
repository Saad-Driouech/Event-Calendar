# Generated by Django 3.0.8 on 2021-07-27 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0017_auto_20210726_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='location',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='courses',
        ),
        migrations.AddField(
            model_name='course',
            name='venue_type',
            field=models.CharField(choices=[('1', 'Classroom'), ('2', 'IT'), ('3', 'Auditorium'), ('4', 'Conference Room'), ('5', 'Laboratory')], default=1, max_length=20),
        ),
        migrations.AddField(
            model_name='venue',
            name='capacity',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='venue',
            name='type',
            field=models.CharField(choices=[('1', 'Classroom'), ('2', 'IT'), ('3', 'Auditorium'), ('4', 'Conference Room'), ('5', 'Laboratory')], default=1, max_length=20),
        ),
    ]
