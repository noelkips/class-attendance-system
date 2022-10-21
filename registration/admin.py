from django.contrib import admin
from .models import Registration, Attendance


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('unit', 'user', 'year', 'semester')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'lecture')


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Attendance, AttendanceAdmin)
