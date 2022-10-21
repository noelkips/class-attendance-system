from django.contrib import admin
from learningAttendance.models import Course, School, Unit,Lecture

admin.site.register(School)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lecture)

