from django.urls import path

from . import views

app_name = 'calendarapp'
urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('session/new/', views.create_session, name='session_new'),
    path('course/new/', views.create_course, name='course_new'),
    path('venue/new/', views.create_venue, name='venue_new'),
    path('session/edit/<int:pk>/', views.SessionEdit.as_view(), name='session_edit'),
    path('session/<int:session_id>/details/', views.session_details, name='session-detail'),
    path('professor/create/', views.create_professor, name='professor_new'),
    path('student/create/', views.create_student, name='student_new'),
    path('groupe/create/', views.create_groupe, name='groupe_new'),
    path('event/<int:pk>/remove', views.EventMemberDeleteView.as_view(), name="remove_event"),
    path('availability/create/',views.create_availablity, name='availability_new'),
    path('preference/create/',views.create_preference, name='preference_new'),
]