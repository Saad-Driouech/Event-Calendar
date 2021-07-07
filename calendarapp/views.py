# cal/views.py

from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import *
from .utils import Calendar
from .forms import AddProfessorForm, DayAvailabilityForm, SessionForm, AddCourseFrom

@login_required(login_url='signup')
def index(request):
    return HttpResponse('hello')

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def check_professor_availability(start_time, end_time, course, professor):
    if(course in professor.course.all()):
        print("professor teaches course")
        day = professor.dayavailability_set.all().filter(day=start_time.strftime("%w"))
        if day:
            if(start_time.time() >= day[0].start_time and end_time.time() <= day[0].end_time):
                temp = (start_time.isoweekday()+1)%6 
                sessions = Session.objects.filter(start_time__week_day=temp,  professor=professor)
                print("all sessions", sessions)
                for sess in sessions:
                    print("session", sess)
                    if (sess.start_time.strftime('%H:%M') <= start_time.strftime('%H:%M') and start_time.strftime('%H:%M') <= sess.end_time.strftime('%H:%M')) or (sess.start_time.strftime('%H:%M') <= end_time.strftime('%H:%M') and end_time.strftime('%H:%M') <= sess.end_time.strftime('%H:%M')):
                        print("this session is within the professor's schedule, however it is in a conflict with an already existing session")
                        return 0
            else:
                    print("The professor will not be available during the session")
                    return 0
        else:
            print("the professor does not teach in this day")
            return 0
    else:
        print("Professor doesn't teach the course")
        return 0
    return 1

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'signup'
    model = Session
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(self.request.GET.get('month', None))
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

@login_required(login_url='signup')
def create_session(request):    
    form = SessionForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        course = form.cleaned_data["course"]
        professor = form.cleaned_data['professor']
        flag = check_professor_availability(start_time, end_time, course, professor)
        if flag == 1:
            print("there is no conflict with any of the professor's sessions")
            Session.objects.get_or_create(
                course=course,
                professor=professor,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time
            )
            return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'event.html', {'form': form})

"""@login_required(login_url='signup')
def create_event(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.cleaned_data['user'] = request.user
        form.save()
        form = EventForm()
    context = {
        "form": form
    }
    return render(request, 'event.html', context)
"""

@login_required(login_url='singup')
def create_course(request):
    form = AddCourseFrom(request.POST or None)
    if request.POST and form.is_valid():
        title=form.cleaned_data['title']
        code=form.cleaned_data['code']
        Course.objects.get_or_create(
            title=title,
            code=code
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, "course.html", {"form": form})


class SessionEdit(generic.UpdateView):
    model = Session
    fields = ['professor', 'course', 'title', 'description', 'start_time', 'end_time']
    template_name = 'event.html'

@login_required(login_url='signup')
def session_details(request, event_id):
    session = Session.objects.get(id=event_id)
    professor = Professor.objects.filter(session=session)
    context = {
        'event': session,
        'professor': professor
    }
    return render(request, 'event-details.html', context)

def create_professor(request):
    forms = AddProfessorForm(request.POST or None)
    if request.POST and forms.is_valid():
        name = forms.cleaned_data['name']
        course = forms.cleaned_data['course']
        rank = forms.cleaned_data['rank']
        print("course", course)
        Professor.objects.get_or_create(
            name=name,
            course__in=course,
            rank = rank
        )
        # prof = Professor(name=name)
        # prof.save() 
        # prof.course.add(course) 
        return redirect('calendarapp:calendar')
    return render(request, 'add_member.html', {"form": forms})

"""def assign_professor(request, session_id):
    forms = AddProfessorForm()
    if request.method == 'POST':
        forms = AddProfessorForm(request.POST)
        if forms.is_valid():
            session = Session.objects.get(id=session_id)
            name = forms.cleaned_data['name']
            start_time = forms.cleaned_data['start_time']
            end_time = forms.cleaned_data['end_time']
            if session.start_time <= start_time and session.end_time >= end_time:
                Professor.objects.get_or_create(
                    event=session,
                    name=name,
                    start_time=start_time,
                    end_time=end_time 
                )
                em = Professor.objects.filter(event=session_id)
                print(em[0].session.title)
                return redirect('calendarapp:calendar')
            else:
                print('--------------Member is not available during this time---------------')
        else: 
            print(forms.errors.as_data())
    context = {
        'form': forms
    }
    return render(request, 'add_member.html', context)"""

"""def assign_prof_to_session(request, session_id):
    session = Session.objects.get(id=session_id)
    course = session.course
    professors = Professor.objects.filter(course=course, start_time__lte=session.start_time, end_time__gte=session.end_time)
    if professors.count > 0:
        Professor.objects.update_or_create(

        )
    context = {
        'professors': professors
    }
    return render
"""

def create_availablity(request):
    form = DayAvailabilityForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DayAvailabilityForm()
    context = {
        "form": form
    }
    return render(request, 'create_availability.html', context)

class EventMemberDeleteView(generic.DeleteView):
    model = Professor
    template_name = 'event_delete.html'
    success_url = reverse_lazy('calendarapp:calendar')
