from django.urls import path

from . import views

app_name = 'calendarapp'
urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.create_session, name='event_new'),
    path('event/edit/<int:pk>/', views.SessionEdit.as_view(), name='event_edit'),
    path('event/<int:event_id>/details/', views.session_details, name='event-detail'),
    path('add_eventmember/<int:session_id>', views.assign_professor, name='add_eventmember'),
    path('event/<int:pk>/remove', views.EventMemberDeleteView.as_view(), name="remove_event"),
]