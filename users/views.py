from os import path
from urllib.request import urlopen

from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import CustomUser
from .forms import CustomUserCreationForm, UserUpdateForm, UpdateProfilePic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from learningAttendance.models import Course, Unit, Lecture
from registration.models import Registration, Attendance


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('meru_learning:schools_list'))
            elif user.is_staff:
                login(request, user)
                return HttpResponseRedirect(reverse('lecturer_profile'))
            elif user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))  # student_panel
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Your username or password is wrong <br> <a href="">click here to try again</a>")
    else:
        return render(request, 'registration/login.html')


# @login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def my_course_info(request):
    courses = Course.objects.filter(course_name=request.user.course)
    registered_units = Registration.objects.filter(user=request.user)

    if 'profile_pic' in request.POST:
        form = UpdateProfilePic(request.POST, request.FILES)
        if form.is_valid():
            m = CustomUser.objects.get(username=request.user.username)
            m.profile_pic = form.cleaned_data['image']
            m.save()
        return redirect('profile')

    context = {
        "courses": courses,
        "registered_units": registered_units

    }
    return render(request, "profile.html", context)


@login_required
def lecturer_profile(request):
    unit = Unit.objects.filter(lecturer=request.user)
    if 'profile_pic' in request.POST:
        form = UpdateProfilePic(request.POST, request.FILES)
        if form.is_valid():
            m = CustomUser.objects.get(username=request.user.username)
            m.profile_pic = form.cleaned_data['image']
            m.save()
        return redirect('lecturer_profile')
    context = {
        "units": unit,

    }
    return render(request, 'lecturer/lecturer_profile.html', context)


def update_lecturer_pic(request):
    return render(request, "profile_updates/update_lecturer_pic.html")


class LecturesListView(DetailView):
    context_object_name = 'units'
    model = Unit
    template_name = "lecturer/lectures.html"


class LecturesAttendanceView(DetailView):
    context_object_name = 'units'
    model = Unit
    template_name = "lecturer/lectures_attendance.html"


class LectureDetailView(DetailView):
    context_object_name = 'lecture'
    model = Lecture
    template_name = "lecturer/lecture_detail.html"


def lecturer_units(request):
    unit = Unit.objects.filter(lecturer=request.user)
    context = {
        "units": unit,

    }
    return render(request, "lecturer/lecturer_units.html", context)


def update_profile_pic(request):
    return render(request, "profile_updates/update_profile_pic.html")


class StudentUnitsList(DetailView):
    context_object_name = 'courses'
    model = Course
    template_name = "student/all_units.html"


class UserListView(ListView):
    model = CustomUser
    template_name = 'updates/all_students.html'
    context_object_name = "users"


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'updates/user_new.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users_list')


#
# class UserUpdateView(UpdateView):
#     model = CustomUser
#     template_name = 'updates/user_edit.html'
#     fields = ['first_name', 'last_name', 'username', 'email', 'year', 'school', 'course', 'semester', 'profile_pic',]

class UserUpdateView(UpdateView, SuccessMessageMixin):
    model = CustomUser
    template_name = 'updates/user_edit.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_list')
    success_message = 'update success'


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'updates/user_delete.html'
    success_url = reverse_lazy('users_list')


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'updates/user_detail.html'


class StudentLecturesList(DetailView):
    context_object_name = 'units'
    model = Unit
    template_name = "student/lectures.html"


def student_attendance_report(request, slug):
    unit = get_object_or_404(Unit, slug=slug)
    all_lectures = Lecture.objects.filter(unit=unit)
    attendance_list = Attendance.objects.filter(user=request.user)
    registered_lectures = []
    attended_lectures = []

    for lec in all_lectures:
        registered_lectures.append(lec)
    for attendance in attendance_list:
        lecture = attendance.lecture
        attended_lectures.append(lecture)
    total_attendance = f'you have attended {len(attendance_list)} of {len(registered_lectures)} lectures'
    percentage = (len(attendance_list) / len(registered_lectures)) * 100
    if percentage >= 70:
        exam_qualification = 'you meet the minimum class attendance requirement to sit for exams'
    else:
        exam_qualification = 'you don\'t meet the minimum class attendance requirement to sit for exams'

    context = {
        "unit": unit,
        'exam_qualification': exam_qualification,
        "total_attendance": total_attendance,
        "lectures": attendance_list,
        "all_lectures": registered_lectures,
    }
    return render(request, "student/lectures_attendance_report.html", context)


def registered_units_view(request):
    registered_units = Registration.objects.filter(user=request.user)
    return render(request, 'student/units.html',
                  {"units": registered_units, })
