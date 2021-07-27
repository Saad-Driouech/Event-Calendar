from datetime import datetime
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.urls import reverse
from django.contrib.auth.models import GroupManager, User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    VENUE_CHOICES = (
        ('1', 'Classroom'),
        ('2', 'IT'),
        ('3', 'Auditorium'),
        ('4', 'Conference Room'),
        ('5', 'Laboratory'),
    )
    title = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    venue_type = models.CharField(max_length=20, choices=VENUE_CHOICES, default=1)

    def __str__(self):
        return str(self.title)

class Venue(models.Model):
    VENUE_CHOICES = (
        ('1', 'Classroom'),
        ('2', 'IT'),
        ('3', 'Auditorium'),
        ('4', 'Conference Room'),
        ('5', 'Laboratory'),
    )
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=VENUE_CHOICES, default=1)
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.name)

class Professor(models.Model):
    RANK_CHOICES = (
        ('1', 'Rank 1'),
        ('2', 'Rank 2'),
        ('3', 'Rank 3'),
    )
    name = models.CharField(max_length=100)
    course= models.ManyToManyField(Course)
    rank = models.CharField(max_length=6, choices=RANK_CHOICES, default='1')
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.name)

class DayPreferences(models.Model):
    DAY_CHOICES = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('0', 'Sunday'),
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=15, choices=DAY_CHOICES)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.professor) + ': ' + str(self.get_day_display())

class DayAvailability(models.Model):
    DAY_CHOICES = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('0', 'Sunday'),
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=15, choices=DAY_CHOICES)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.professor) + ': ' + str(self.get_day_display()) 

class Students(models.Model):
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)
    
class Groupe(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Students)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return str(self.name)

class Session(models.Model): 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Groupe, on_delete=models.CASCADE, default=1)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.course) + ' ' + str(self.group.id)
    
    def get_absolute_url(self):
        return reverse('calendarapp:session-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('calendarapp:session-detail', args=(self.id,))
        return f'<a href="{url}"> {self.course} {self.group.id} </a>'