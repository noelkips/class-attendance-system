from django.urls import path
from . import views
from learningAttendance.views import StudentListView


urlpatterns = [
    path('login/', views.user_login, name='login'),
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
    path('lecturer/units/<str:unit>/<slug:slug>/',
         views.LectureDetailView.as_view(), name='lecture_detail'
         ),



    path('students/', views.UserListView.as_view(), name="users_list"),

    path('students/new/', views.UserCreateView.as_view(), name='user_new'),
    path('students/<slug:slug>/', views.UserDetailView.as_view(), name="user_detail"),
    path('students/<slug:slug>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('students/<slug:slug>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

]
