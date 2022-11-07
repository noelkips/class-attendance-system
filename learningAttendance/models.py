from tabnanny import verbose
from django.db import models
from django.template.defaultfilters import slugify
import os
# from users.models import CustomUser
from django.urls import reverse
from django.conf import settings

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


def save_school_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    filename = 'School_Pictures/{}.{}'.format(instance.name, ext)
    return os.path.join(upload_to, filename)


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_school_image, blank=True, verbose_name='school image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('meru_learning:school_detail', args=[str(self.pk)])


def save_course_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    filename = 'course_pictures/{}.{}'.format(instance.course_name, ext)
    return os.path.join(upload_to, filename)


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to=save_course_image, blank=True, verbose_name='course image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.course_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('meru_learning:courses_list', args=[slugify(self.school.slug)])

def course_unit_pdf(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.course:
        filename = 'course_pdf/{}/{}.{}'.format(instance.course, instance.course, ext)
        if os.path.exists(filename):
            new_name = str(instance.course) + str('1')
            filename = 'course_pdf/{}/{}.{}'.format(instance.course, new_name, ext)
    return os.path.join(upload_to, filename)

class CourseUnits(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    unit_pdf = models.FileField(upload_to=course_unit_pdf, verbose_name='Unit PDF', blank=True)


def save_unit_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.unit_name:
        filename = 'Unit_Pictures/{}.{}'.format(instance.unit_name, ext)
    return os.path.join(upload_to, filename)


class Unit(models.Model):
    unit_name = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    slug = models.SlugField(null=True, blank=True)
    year = models.IntegerField(choices=academic_years, default=1)
    semester = models.IntegerField(choices=semesters, default=1)
    image = models.ImageField(upload_to=save_unit_image, blank=True, verbose_name='unit image')
    is_offered = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Lecture", default=1)

    def __str__(self):
        return self.unit_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.unit_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'slug':self.course.slug,
            'school':self.course.school.slug,
        }
        return reverse('meru_learning:units_list', kwargs=kwargs)


def save_lecture_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lecture_name:
        filename = 'lecture_files/{}/{}.{}'.format(instance.lecture_name, instance.lecture_name, ext)
        if os.path.exists(filename):
            new_name = str(instance.lecture_name) + str('1')
            filename = 'Lecture_images/{}/{}.{}'.format(instance.lecture_name, new_name, ext)
    return os.path.join(upload_to, filename)


class Lecture(models.Model):
    lecture_name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Lecturer")
    created_at = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lectures')
    position = models.PositiveSmallIntegerField(verbose_name='Chapter no.')
    slug = models.SlugField(null=True, blank=True)
    # position represents chaters...1 is chapter one and so on
    video = models.FileField(upload_to=save_lecture_files, verbose_name='video', blank=True)
    ppt = models.FileField(upload_to=save_lecture_files, verbose_name='presentation', blank=True, null=True)
    notes = models.FileField(upload_to=save_lecture_files, verbose_name='notes', blank=True, null=True)
    
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.lecture_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.lecture_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            "slug": self.slug,
            'unit':self.unit.slug,
            'course':self.unit.course.slug,
            'school':self.unit.course.school.slug,
        }
        return reverse('meru_learning:lectures_detail', kwargs=kwargs)
