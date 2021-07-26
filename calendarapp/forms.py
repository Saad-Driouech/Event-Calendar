from django.db.models import fields
from django.forms import ModelForm, DateInput, widgets, TimeInput
from calendarapp.models import Course, DayPreferences, Groupe, Professor, Session, DayAvailability, Students
from django import forms

class SessionForm(ModelForm):
  class Meta:
    model = Session
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields= ['start_time', 'end_time', 'group']

  def __init__(self, *args, **kwargs):
    super(SessionForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class SignupForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AddProfessorForm(forms.ModelForm):
  class Meta:
    model = Professor

    fields = ['name', 'course', 'rank']

class AddCourseFrom(forms.ModelForm):
  class Meta:
    model = Course
    fields = ['title', 'code']

class AddGroupeForm(forms.ModelForm):
  class Meta:
    model = Groupe
    fields = ['name', 'students', 'courses']

class AddStudentsForm(forms.ModelForm):
  class Meta:
    model = Students
    fields = ['name', 'level']


class DayAvailabilityForm(forms.ModelForm):
  class Meta:
    model = DayAvailability

    widgets = {
      'start_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
      'end_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
    }
    fields= ['professor', 'day', 'start_time', 'end_time']

  def __init__(self, *args, **kwargs):
    super(DayAvailabilityForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%H:%M',)
    self.fields['end_time'].input_formats = ('%H:%M',)

  
class DayPreferenceForm(forms.ModelForm):
  class Meta:
    model = DayPreferences

    widgets = {
      'start_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
      'end_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
    }
    fields= ['professor', 'day', 'start_time', 'end_time']

  def __init__(self, *args, **kwargs):
    super(DayPreferenceForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%H:%M',)
    self.fields['end_time'].input_formats = ('%H:%M',)
