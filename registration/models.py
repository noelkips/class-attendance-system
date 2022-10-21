import os

from django.db import models
from django.conf import settings
from django.urls import reverse

from learningAttendance.models import Unit, Lecture

semesters = (
    (1, 1),
    (2, 2),
    (3, 3),
)
academic_years = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),

)


class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Student")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='registrations')
    year = models.IntegerField(choices=academic_years, default=1)
    semester = models.IntegerField(choices=semesters, default=1)

    def __str__(self):
        return f'Your registration for unit ({self.unit}) was Successful '

    #
    def get_absolute_url(self):
        return reverse('meru_learning:schools_list')


class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Student")
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateTimeField(auto_now_add=True)

#
# class ExamQualified(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Student")
#     registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
#     attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
#     lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='attendance')
#     date = models.DateTimeField(auto_now_add=True)