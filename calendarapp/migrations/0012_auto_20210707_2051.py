# Generated by Django 3.0.8 on 2021-07-07 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0011_professor_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.Professor'),
        ),
    ]