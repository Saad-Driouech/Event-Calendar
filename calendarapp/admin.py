from django.contrib import admin
from calendarapp.models import Course, Professor, Session

class EventMemberAdmin(admin.ModelAdmin):
    model = Professor
    list_display = ['event', 'name']

admin.site.register(Session)
admin.site.register(Professor, EventMemberAdmin)
admin.site.register(Course)
