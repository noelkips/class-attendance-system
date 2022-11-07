from django.urls import path
from . import views
from learningAttendance.views import StudentListView


urlpatterns = [
    path('', views.login_request, name='login_request'),
    path('student_login/', views.student_login, name='student_login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('logout/', views.user_logout, name='logout'),


    path('profile/', views.my_course_info, name="profile"),
    path('profile>/<slug:slug>/units',
         views.StudentUnitsList.as_view(), name='all_units'
         ),
    path("profile/registered_units/", views.registered_units_view, name="registered_units"),
    path('profile/registered_units/<slug:slug>/attendance/',
         views.student_attendance_report, name='student_attendance_report'
         ),
    path('profile/registered_units/<slug:slug>/',
         views.StudentLecturesList.as_view(), name='student_lectures'
         ),

    path('update_profile_pic', views.update_profile_pic, name="update_profile_pic"),



    path('lecturer/', views.lecturer_profile, name="lecturer_profile"),
    path('profile_update', views.update_lecturer_pic, name="update_lecturer_pic"),
    path('lecturer/units/', views.lecturer_units, name="lecturer_units"),
    path('lecturer/units/<slug:slug>/',
         views.LecturesListView.as_view(), name='lecturer_lectures'
         ),
    path('lecturer/units/<slug:slug>/attendance',
         views.LecturesAttendanceView.as_view(), name='lecturer_attendance'
         ),  
     path('lecturer/units_attendance/', views.lecturer_units_report, name="lecturer_units_report"),
     path('lecturer/<slug:slug>/units_attendance/', views.lecturer_lectures_report, name="lecturer_lectures_report"),
     path('lecturer/units/<slug:slug>/attendance_report',
         views.lecturer_student_attendance_report, name='lecture_attendance_report'
         ),
    path('lecturer/units/<str:unit>/<slug:slug>/',
         views.LectureDetailView.as_view(), name='lecture_detail'
         ),



    path('students/', views.UserListView.as_view(), name="users_list"),

    path('students/new/', views.UserCreateView.as_view(), name='user_new'),
    path('students/<slug:slug>/', views.UserDetailView.as_view(), name="user_detail"),
    path('students/<slug:slug>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('students/<slug:slug>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
     path('students/units/<str:unit>/<slug:slug>/lectures/',
         views.StudentLectureDetailView.as_view(), name='student_lecture_detail'
         ),

]
