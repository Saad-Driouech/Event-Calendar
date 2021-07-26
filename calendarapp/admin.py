from django.contrib import admin
from calendarapp.models import Course, DayAvailability, DayPreferences, Groupe, Professor, Session, Students, Venue

"""class EventMemberAdmin(admin.ModelAdmin):
    model = Professor
    list_display = ['event', 'name']"""

admin.site.register(Session)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Venue)
admin.site.register(DayAvailability)
admin.site.register(DayPreferences)
admin.site.register(Groupe)
admin.site.register(Students)
