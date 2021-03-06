# Generated by Django 3.0.8 on 2021-07-15 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0014_daypreferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='session',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.Course'),
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('courses', models.ManyToManyField(to='calendarapp.Course')),
                ('students', models.ManyToManyField(to='calendarapp.Students')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.Groupe'),
        ),
    ]
