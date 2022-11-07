from django.urls import path
from . import views
from registration.views import UnitRegisteredStudents, UnitRegistrationView

app_name = 'meru_learning'
urlpatterns = [

    path('students_list/', views.StudentListView.as_view(), name="students_list"),

    # urls for school
    path('', views.schools_list_view, name="schools_list"),
    path('<int:pk>/', views.SchoolDetailView.as_view(), name="school_detail"),
    path('new/', views.SchoolCreateView.as_view(), name='school_create'),
    path('<int:pk>/edit/', views.SchoolUpdateView.as_view(), name='school_update'),
    path('<int:pk>/delete/', views.SchoolDeleteView.as_view(), name='school_delete'),

    # urls for course
    path('<slug:slug>/new/', views.CourseCreateView.as_view(), name='course_create'),
    path('<slug:slug>/', views.CoursesListView.as_view(), name='courses_list'),
    
    path('<slug:slug>/<int:pk>/', views.CourseDetailView.as_view(), name="course_detail"),
    path('<slug:slug>/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<slug:slug>/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # urls for units
    path('<str:school>/<slug:slug>/',
         views.UnitsListView.as_view(), name='units_list'
         ),
    path('<str:school>/<slug:slug>/students/',
         views.StudentListView.as_view(), name='students'
         ),
    path('<str:school>/<slug:slug>/new/', views.UnitCreateView.as_view(), name='unit_create'),
    path('<str:school>/<slug:slug>/<int:pk>/', views.UnitDetailView.as_view(), name="unit_detail"),
    path('<str:school>/<slug:slug>/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='unit_update'),
    path('<str:school>/<slug:slug>/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),


     #urls for lectures
    path('<str:school>/<str:course>/<slug:slug>/',
         views.LecturesListView.as_view(), name='lectures_list'
    ),
    path('<str:school>/<str:course>/<slug:slug>/new/', views.LectureCreateView.as_view(), name='lecture_create'),
     path('<str:school>/<str:course>/<str:unit>/<slug:slug>/',
         views.LectureDetailView.as_view(), name='lectures_detail'
         ),
    path('<str:school>/<str:course>/<slug:slug>/<int:pk>/edit/', views.LectureUpdateView.as_view(), name='lecture_update'),
    path('<str:school>/<str:course>/<slug:slug>/<int:pk>/delete/', views.LectureDeleteView.as_view(), name='lecture_delete'),
    


    path('<str:school>/<str:course>/<str:unit>/<slug:slug>/attendance/',
         views.AttendanceListView.as_view(), name='attendance_list'
         ),
    path('<str:school>/<str:course>/<slug:slug>/students',
         UnitRegisteredStudents.as_view(), name='unit_student_list'
         ),
    path('<str:school>/<str:course>/<slug:slug>/students/new',
         UnitRegistrationView.as_view(), name='unit_student_registration'
         ),
   

]
