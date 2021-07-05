from datetime import datetime
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    title = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)

class Professor(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    course= models.ManyToManyField(Course)
    created_date = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ['event', 'name']

    def __str__(self):
        return str(self.user)

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('calendarapp:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('calendarapp:event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    """def validate_professor(self):
        professors = Professor.filter(course=self.course)
        if self.professor not in professors:
            raise ValidationError(
                _('The professor you chose does not teach this course'),
            )"""