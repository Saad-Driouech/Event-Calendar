from django.contrib import admin
from calendarapp.models import Course, DayAvailability, Professor, Session, Venue

"""class EventMemberAdmin(admin.ModelAdmin):
    model = Professor
    list_display = ['event', 'name']"""

admin.site.register(Session)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Venue)
admin.site.register(DayAvailability)
