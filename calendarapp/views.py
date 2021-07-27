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
from django.db.models import Q

from .models import *
from .utils import Calendar
from .forms import AddGroupeForm, AddProfessorForm, AddStudentsForm, AddVenueFrom, DayAvailabilityForm, DayPreferenceForm, SessionForm, AddCourseFrom

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

def check_group_availability(group, start_time, end_time):
    students = group.students.all()
    criterion1 = Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
    criterion2 = Q(start_time__lte=end_time) & Q(end_time__gte=end_time)
    for student in students:
        #checking for each student if they are in a group that has a session conflicting with this session
        student_groups =  student.groupe_set.all()
        for student_group in student_groups:
            group_sessions = Session.objects.filter(criterion1 | criterion2, group=student_group)
            if group_sessions.exists():
                print("Student: ", student, " has another session with group: ", student_group, " during this time")
                return 0
    return 1

def check_course_eligibility(group):
    eligible_courses = []
    group_courses = group.courses.all()
    #filtering through eligible courses leaving only courses that are not taken by any students in another session
    for group_course in group_courses:
        print("course being tested: ", group_course)
        flag = 1
        students = group.students.all()
        for student in students:
            student_groups = student.groupe_set.all()
            for student_group in student_groups:
                if Session.objects.filter(group=student_group, course=group_course).exists():
                    print(student, "has already a session of", group_course, "with ", student_group)
                    flag = 0
                    break
            if flag == 0:
                break
            else:
                if not group_course in eligible_courses:
                    eligible_courses.append(group_course)
    return eligible_courses

def assign_course_and_professor_to_session(group, start_time, end_time):
    available_prof = None
    prof_course = None
    criterion1 = Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
    criterion2 = Q(start_time__lte=end_time) & Q(end_time__gte=end_time)
    eligible_courses = check_course_eligibility(group)
    print("eligible courses: ", eligible_courses)
    if len(eligible_courses) > 0:
        for eligible_course in eligible_courses:
            print("current eligible course: ", eligible_course)
            professors = Professor.objects.filter(course=eligible_course).order_by('rank')
            print("Professors who teach this course", professors)
            if professors.exists():
                for prof in professors:
                    print("professor: ", prof)
                    day_availabilities = prof.dayavailability_set.all().filter(day=start_time.strftime("%w"), start_time__lte=start_time.time(), end_time__gte=end_time.time())
                    if day_availabilities.exists():
                        prof_sessions = Session.objects.filter(criterion1 | criterion2,  professor=prof)
                        print("conflicting sessions: ", prof_sessions)
                        if prof_sessions.exists():
                            print("this session is within the professor's schedule, however it is in a conflict with an already existing session")
                        else:
                            available_prof = prof
                            prof_course = eligible_course
                            day_preferences = prof.daypreferences_set.all().filter(day=start_time.strftime("%w"), start_time__lte=start_time.time(), end_time__gte=end_time.time())
                            if day_preferences.exists():
                                print("the professor prefers to teach at this time")
                                print("professor", prof.name, "was assigned this session")
                                return prof, eligible_course
                            else:
                                print("The professor does not prefer to teach during this time")          
                    else:
                        print("the professor does not teach at this time")
            
                if available_prof != None:
                    print("professor", prof.name, "was assigned this session")
                    return available_prof, prof_course
            else:
                print("No professor teaches this course")
            if eligible_course == eligible_courses[-1]:
                print("there is a list of eligible professors. However, either none of them is available or some courses does not have a professor attributed")
    else:
        print("There is no eligible courses")
    return None, None

def check_venue_availability(group, course, start_time, end_time):
    number_students = group.students.all().count()
    criterion1 = Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
    criterion2 = Q(start_time__lte=end_time) & Q(end_time__gte=end_time)
    eligible_venues = Venue.objects.filter(capacity__gte=number_students, type=course.venue_type).order_by("capacity")
    if eligible_venues.exists():
        print("Eligble venues: ", eligible_venues)
        for eligible_venue in eligible_venues:
            sessions_in_venue = Session.objects.filter(criterion1 | criterion2, venue=eligible_venue)
            if not sessions_in_venue.exists():
                print("This session will be held in this venue:", eligible_venue)
                return eligible_venue
        print("All the venues in which this session can be held will not be available during the time of the session")
        return None
    else:
        print("There is no venue wherein this session can be hold")
        return None

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
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        group = form.cleaned_data["group"]
        flag = check_group_availability(group, start_time, end_time)
        if flag == 1:
            print("all students in this group are available")
            professor, course = assign_course_and_professor_to_session(group, start_time, end_time)
            if professor != None:
                venue = check_venue_availability(group, course, start_time, end_time)
                if venue != None:
                    Session.objects.get_or_create(
                        title=str(course) + ' ' + str(group.id),
                        start_time= start_time,
                        end_time= end_time,
                        group = group,
                        professor = professor,
                        course = course,
                        venue = venue
                    )
                    print("Session created successfully")
                else:
                    print("No venue is available during this time")
            else: 
                print("No professor is available during this time")
        else:
            print("not all students in this group are available")
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'session.html', {'form': form})

@login_required(login_url='singup')
def create_course(request):
    form = AddCourseFrom(request.POST or None)
    if request.POST and form.is_valid():
        title=form.cleaned_data['title']
        code=form.cleaned_data['code']
        venue_type=form.cleaned_data['venue_type']
        Course.objects.get_or_create(
            title=title,
            code=code,
            venue_type=venue_type
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, "add_course.html", {"form": form})

def create_student(request):
    form = AddStudentsForm(request.POST or None)
    if request.POST and form.is_valid():
        name=form.cleaned_data['name']
        level=form.cleaned_data['level']
        Students.objects.get_or_create(
            name=name,
            level=level
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, "add_student.html", {"form": form})

def create_groupe(request):
    form = AddGroupeForm(request.POST or None)
    if request.POST and form.is_valid():
        name=form.cleaned_data['name']
        students=form.cleaned_data['students']
        courses=form.cleaned_data['courses']
        groupe = Groupe(name=name)
        groupe.save()
        for student in students:
            groupe.students.add(student)
        for course in courses:
            groupe.courses.add(course)
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, "add_groupe.html", {"form": form})

@login_required(login_url='singup')
def create_venue(request):
    form = AddVenueFrom(request.POST or None)
    if request.POST and form.is_valid():
        name=form.cleaned_data['name']
        type=form.cleaned_data['type']
        capacity=form.cleaned_data['capacity']
        Venue.objects.get_or_create(
            name=name,
            type=type,
            capacity=capacity
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, "add_venue.html", {"form": form})

class SessionEdit(generic.UpdateView):
    model = Session
    fields = ['professor', 'course', 'title', 'start_time', 'end_time', 'group', 'venue']
    template_name = 'session.html'

@login_required(login_url='signup')
def session_details(request, session_id):
    session = Session.objects.get(id=session_id)
    professor = Professor.objects.filter(session=session)
    context = {
        'session': session,
        'professor': professor
    }
    return render(request, 'session-details.html', context)

def create_professor(request):
    forms = AddProfessorForm(request.POST or None)
    if request.POST and forms.is_valid():
        name = forms.cleaned_data['name']
        courses = forms.cleaned_data['course']
        rank = forms.cleaned_data['rank']
        prof = Professor(name=name, rank=rank)
        prof.save() 
        for course in courses:
            prof.course.add(course) 
        return redirect('calendarapp:calendar')
    return render(request, 'add_member.html', {"form": forms})

def create_availablity(request):
    form = DayAvailabilityForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DayAvailabilityForm()
    context = {
        "form": form
    }
    return render(request, 'create_availability.html', context)

def create_preference(request):
    form = DayPreferenceForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DayPreferenceForm
    context = {
        "form": form
    }
    return render(request, 'create_preference.html', context)

class EventMemberDeleteView(generic.DeleteView):
    model = Professor
    template_name = 'event_delete.html'
    success_url = reverse_lazy('calendarapp:calendar')
