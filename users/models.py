from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.urls import reverse
from django.conf import settings
from django.template.defaultfilters import slugify
from learningAttendance.models import School, Course

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


def profile_pic_path(self, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    filename = 'profile_pictures/{}.{}'.format(self.pk, ext)
    return os.path.join(upload_to, filename)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    username = models.CharField(max_length=30, unique=True, verbose_name="Registration/Payroll Number")
    slug = models.SlugField(blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='schools',  blank=True, null=True,
                               verbose_name='Student Faculty',
                               help_text="only applicable to student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='users', blank=True, null=True,
                               verbose_name='Student Course'
                               , help_text="only applicable to student")
    year = models.IntegerField(choices=academic_years, blank=True, null=True, help_text="only applicable to student")
    semester = models.IntegerField(choices=semesters, blank=True, null=True, help_text="only applicable to student")
    profile_pic = models.ImageField(upload_to=profile_pic_path, verbose_name='profile picture', blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text='only applicable to lecturer.',
                                   verbose_name='Lecturer')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users_list')
