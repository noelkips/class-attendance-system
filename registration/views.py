from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (DetailView, CreateView, DeleteView, UpdateView)

from .models import Unit, Registration, Attendance
from learningAttendance.models import Course, Lecture
from users.models import CustomUser

# imports for recognition
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


class UnitsListView(DetailView):
    context_object_name = 'courses'
    model = Course
    template_name = "all_units.html"


class UnitRegisteredStudents(DetailView):
    context_object_name = 'units'
    model = Unit
    template_name = "registration/unit_students.html"


def registered_units_view(request):
    if request.user.is_staff:
        registered_units = Registration.objects.all()
    else:
        registered_units = Registration.objects.filter(user=request.user)
    return render(request, 'registration/registered_units.html',
                  {"registered_units": registered_units})


def available_units_for_registration(request, slug):
    units_to_register = []
    registered_units = []
    unit_list_info = Unit.objects.filter(course=request.user.course)
    registration_info = Registration.objects.filter(user=request.user)
    for obj in registration_info:
        registered_units.append(obj.unit)
    for unit in unit_list_info:
        if unit in registered_units:

            return HttpResponse(f'There are currently no units for you to register <br> this is because you have '
                                f'either reached the maximum limit or your profile is not updated<br>consider visiting'
                                f' admin')
        else:
            units_to_register.append(unit)
    context = {
        "units_to_register": units_to_register,
    }

    return render(request, "registration/available_units_for_registration.html",
                  context)


def registration(request):
    try:
        units_to_register = []
        registered_units = []
        unit_list = Unit.objects.filter(course=request.user.course)
        registration_info = Registration.objects.filter(user=request.user)
        for obj in registration_info:
            registered_units.append(obj.unit)
        for unit in unit_list:
            if unit in registered_units:
                pass
            else:
                units_to_register.append(unit)
        for unit in units_to_register:
            if unit.semester == request.user.semester and unit.is_offered == True:
                if len(registered_units) > 10:
                    return HttpResponse("You have reached the maximum number of units")
                else:
                    register = Registration.objects.create(
                        unit=unit,
                        user=request.user,
                        profile_pic=request.user.profile_pic,
                        year=unit.year,
                        semester=unit.semester,
                    )
                    register.save()
                    return HttpResponse(register)
    except HttpResponse:
        HttpResponse("You have already registered for this unit, <a>please go back and try again</>")


class RegistrationDeleteView(DeleteView):
    model = Registration
    template_name = 'registration/delete_unit.html'
    success_url = reverse_lazy('registration:registered_units')


# register students for a unit
# used by admin
class UnitRegistrationView(CreateView):
    model = Registration
    template_name = 'registration/unit_registration.html'
    # success_url = reverse_lazy('meru_learning:unit_student_list'course=courses.slug school=courses.school)
    fields = '__all__'


class AttendanceRequest(CreateView):
    model = Attendance
    template_name = 'attendance/attendance_request.html'
    fields = ['lecture', ]


def class_attendance(request, slug):
    lecture = get_object_or_404(Lecture, slug=slug)
    path = 'media/images/profile_pictures'
    images = []
    students_names = []
    image_list = os.listdir(path)

    for cl in image_list:
        current_image = cv2.imread(f'{path}/{cl}')
        images.append(current_image)
        students_names.append(os.path.splitext(cl)[0])

    def findEncodings(images):
        encode_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list

    def mark_attendance(pk):
        with open(f'media/Images/attendance/{lecture}.csv', 'w+') as f:
            registered_students = []
            lecture_attendance_list = []
            registrations = Registration.objects.filter(unit=lecture.unit)
            student = CustomUser.objects.filter(pk=pk)
            all_attendance = Attendance.objects.filter(lecture=lecture)
            for obj in registrations:
                registered_students.append(obj.user.pk)
            for obj in student:
                student_attending = obj
                user_pk = obj.pk
            for attendance in all_attendance:
                lecture_attendance_list.append(attendance.user.pk)
                print("lectures list", lecture_attendance_list)
            if user_pk in registered_students:
                username = student_attending.username
                first_name = student_attending.first_name
                last_name = student_attending.last_name
                student_list = f.readlines()
                name_list = []
                for line in student_list:
                    entry = line.split(",")
                    name_list.append(entry[0])
                if username not in name_list:
                    now = datetime.now()
                    date_attended = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{username}, {first_name} {last_name},{date_attended}, {lecture}, {lecture.unit}')
                if user_pk not in lecture_attendance_list:
                    now = datetime.now()
                    date_attended = now.strftime('%H:%M:%S')
                    attended = Attendance.objects.create(
                        user=student_attending,
                        lecture=lecture,
                        date=date_attended,
                    )
                    attended.save()

        # print("student attending , ", student_attending)

    known_encoded_list = findEncodings(images)
    print("Encoding Complete")
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, face_location in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(known_encoded_list, encodeFace)

            faceDis = face_recognition.face_distance(known_encoded_list, encodeFace)
            match_index = np.argmin(faceDis)
            # print(faceDis)
            if matches[match_index]:
                name_pk = students_names[match_index]
                student_name = CustomUser.objects.filter(pk=name_pk)
                for name_to_encode in student_name:
                    name = name_to_encode.username
                    first_name = name_to_encode.first_name.upper()
                    last_name = name_to_encode.last_name.upper()
                    y1, x2, y2, x1 = face_location
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(img, first_name, (x1 + 6, y2 + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, last_name, (x1 + 96, y2 + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                mark_attendance(name_pk)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

# def class_attendance(request, slug):
#     lecture = get_object_or_404(Lecture, slug=slug)
#     attended_lectures = []
#     # lectures_to_add = []
#     # unit_list = Unit.objects.filter(lecturer=request.user)
#     # lecture_lists = Lecture.objects.all()
#     # for lecturet in lecture_lists:
#     #     unit = lecture.unit
#     #     if unit in unit_list:
#     #         lectures_to_add.append(lecturet)
#     #
#     # for lecture_to_mark in lectures_to_add:
#     #     if lecture_to_mark not in attended_lectures:
#     #         lecturet = lecture_to_mark
#     #         attended_lectures.append(lecture_to_mark)
#     #         print("lecture being marked", lecture)
#     #     else:
#     #         attended_lectures.append(lecture_to_mark)
#     #         lecturet = lecture_to_mark
#
#     path = 'media/Images/profile_pictures/'
#     images = []
#     class_names = []
#     image_list = os.listdir(path)
#
#     for cl in image_list:
#         current_img = cv2.imread(f'{path}/{cl}')
#         images.append(current_img)
#         class_names.append(os.path.splitext(cl)[0])
#
#     print("class names", class_names)
#
#     def findEncodings(images):
#         encode_list = []
#         for i, image in enumerate(images):
#             print("index: ", i,)
#         for image in images:
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             print(len(image))
#             encode = face_recognition.face_encodings(image)
#             encode_list.append(encode)
#         return encode_list
#
#     print("total images: ", len(image_list))
#     print("Marking attendance please wait for the webcam")
#     """
#     def markAttendance(pk):
#
#         registered_students = []
#         attended_list = []
#         name_list = Attendance.objects.filter(lecture=lecture)
#         registrations = Registration.objects.filter(unit=lecture.unit)
#         now = datetime.now()
#         date_attended = now.strftime('%H:%M:%S')
#         for user in name_list:
#             student_attended = user.user.pk
#             attended_list.append(student_attended)
#         for obj in registrations:
#             registered_students.append(obj.user.pk)
#             print("registered students", registered_students)
#         for student_attending in registered_students:
#             if student_attending not in attended_list:
#                 student_attending = CustomUser.objects.filter(pk=pk)
#                 for student in student_attending:
#                     user = student
#                     attended = Attendance.objects.create(
#                         user=user,
#                         lecture=lecture,
#                         date=date_attended,
#                     )
#                     attended.save()
#                     print("student attending , ", user)
#
#         # with open(f'attendance/{lecture}.csv', 'w+') as f:
#         #     student_list = f.readlines()
#         #     name_list = []
#         #     for line in student_list:
#         #         entry = line.split(",")
#         #         name_list.append(entry[0])
#         #     if name not in name_list:
#         #         now = datetime.now()
#         #         dtString = now.strftime('%H:%M:%S')
#         #         f.writelines(f'\n{name}, {dtString}, {lecture}, {lecture.unit}')"""
#
#     encode_list_known = findEncodings(images)
#     print("Encoding Complete")
#     cap = cv2.VideoCapture(0)
#
#     while True:
#         success, img = cap.read()
#
#         img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#         img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
#         faces_at_current_frame = face_recognition.face_locations(img_small)
#         encodes_current_frame = face_recognition.face_encodings(img_small, faces_at_current_frame)
#
#         for encodeFace, face_location in zip(encodes_current_frame, faces_at_current_frame):
#             matches = face_recognition.compare_faces(encode_list_known, encodeFace)
#
#             face_distance = face_recognition.face_distance(encode_list_known, encodeFace)
#             match_index = np.argmin(face_distance)
#             # print(faceDis)
#             if matches[match_index]:
#                 name_pk = class_names[match_index]
#                 student_name = CustomUser.objects.filter(pk=name_pk)
#                 for name_to_encode in student_name:
#                     name = name_to_encode.username
#                     first_name = name_to_encode.first_name.upper()
#                     last_name = name_to_encode.last_name.upper()
#                     print(name)
#                     y1, x2, y2, x1 = face_location
#                     y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                     cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#                     cv2.putText(img, first_name, (x1 + 6, y2 + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
#                     cv2.putText(img, last_name, (x1 + 96, y2 + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
#                     # markAttendance(name_pk)
#
#         cv2.imshow('Webcam', img)
#         key = cv2.waitKey(1)
#         if key == 27:
#             break
#         # else:
#         # return HttpResponse(f'attendence for {name} recorded, <br>refresh the page to take another')
#         cap.release()
#         cv2.destroyAllWindows()

#
# def class_attendance_request(request):
#     return render(request, "registration/attendance_request.html")
