from http.client import HTTPResponse
from multiprocessing import context
from tkinter import E
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from .models import School, Unit, Course, Lecture, CourseUnits
from django.views.generic import (DetailView, CreateView, UpdateView, DeleteView)


# Views fo schools (Faculty)
# 1 list
def schools_list_view(request):
    if request.user.is_superuser:
        schools = School.objects.all()
    elif request.user.is_staff:
        schools = None
    else:
        schools = School.objects.filter(name=request.user.school)
    return render(request, "school/school_list_view.html", {"schools": schools})


# 2 detail
class SchoolDetailView(DetailView):
    model = School
    template_name = 'school/school_detail.html'


# 3 new school
class SchoolCreateView(CreateView):
    model = School
    template_name = 'school/school_create.html'
    fields = ['name', 'image', 'description',
              ]


# 4 update existing school
class SchoolUpdateView(UpdateView):
    model = School
    template_name = 'school/school_update.html'
    fields = ['name', 'image', 'description', ]


# 5 delete
class SchoolDeleteView(DeleteView):
    model = School
    template_name = 'school/school_delete.html'
    success_url = reverse_lazy('meru_learning:schools_list')


# Views fo courses
# 1 list
class CoursesListView(DetailView):
    model = School
    context_object_name = 'schools'
    template_name = "course/courses_list_view.html"


# 2 detail
class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'


# 3 new course
class CourseCreateView(CreateView):
    model = Course
    template_name = 'course/course_create.html'
    fields = ['course_name', 'school', 'image', 'description', ]


# 4 update existing course
class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'course/course_update.html'
    fields = ['course_name', 'school', 'image', 'description', ]


# 5 Delete course
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course/course_delete.html'
    success_url = reverse_lazy('meru_learning:schools_list')


# 6 students registered
class StudentListView(DetailView):
    context_object_name = 'courses'
    model = Course
    template_name = "course/students.html"


# Views fo Units
# 1 list
class UnitsListView(DetailView):
    context_object_name = 'courses'
    model = Course
    template_name = "unit/units_list_view.html"


def unit_list_pdf(request, pk):
    units_list =[]
    course = get_object_or_404(Course, pk=pk)
    units = Unit.objects.filter(course=course)
    with open(f'units_pdf/{course.course_name}.csv', 'w+') as f:
        for unit in units:
            units_list.append(unit)
            print(unit)
        for unit_to_add in units_list:
            unit_list = f.readlines()
            unit_names = []
            for line in unit_list:
                entry = line.split(",")
                unit_names.append(entry[0])
            unit = unit_to_add
            if unit not in unit_names:
                f.writelines(f'\n{unit.unit_name}, {unit.course}, {unit.is_offered}, {unit.semester},{unit.lecturer.first_name} {unit.lecturer.last_name}')
                load_files =CourseUnits.objects.create(
                    course=course,
                    unit_pdf=f,
                )
                load_files.save()
    context= {
        "pdf":f,
    }
    return render(request, "course/course_units_pdf.html", context)
          
   


# 2 detail
class UnitDetailView(DetailView):
    model = Unit
    template_name = 'unit/unit_detail.html'


# 3 new unit
# def unit_create_view(request, slug):

class UnitCreateView(CreateView):
    model = Unit
    template_name = 'unit/unit_create.html'
    fields = ['unit_name', 'course', 'year', 'semester', 'image', 'is_offered', 'description', 'lecturer']


# 4 update existing unit
class UnitUpdateView(UpdateView):
    model = Unit
    template_name = 'unit/unit_update.html'
    fields = ['unit_name', 'course', 'year', 'semester', 'image', 'is_offered', 'description', 'lecturer']


# 5 Delete unit
class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'unit/unit_delete.html'
    success_url = reverse_lazy('meru_learning:schools_list')

#views for lecture
#list
class LecturesListView(DetailView):
    context_object_name = 'units'
    model = Unit
    template_name = "lecture/lectures_list_view.html"

# 2 detail
class LectureDetailView(DetailView):
    context_object_name = 'lecture'
    model = Lecture
    template_name = "lecture/lecture_detail_view.html"


# 3 new unit
class LectureCreateView(CreateView):
    model = Lecture
    template_name = 'lecture/lecture_create.html'
    fields = ['lecture_name', 'created_by','position', 'unit', 'video', 'ppt', 'notes']


# 4 update existing lecture
class LectureUpdateView(UpdateView):
    model = Lecture
    template_name = 'lecture/lecture_update.html'
    fields = ['lecture_name', 'created_by','position', 'unit', 'video', 'ppt', 'notes']


# 5 Delete lecture
class LectureDeleteView(DeleteView):
    model = Lecture
    template_name = 'lecture/lecture_delete.html'
    success_url = reverse_lazy('meru_learning:schools_list')





class AttendanceListView(DetailView):
    context_object_name = 'lectures'
    model = Lecture
    template_name = "attendance_list.html"
