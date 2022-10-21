from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path("registered_units", views.registered_units_view, name="registered_units"),
    path('profile/<int:pk>/delete/', views.RegistrationDeleteView.as_view(), name='registration_delete'),
    path('profile/register_unit/', views.registration, name='unit_registration_new'),
    path('profile/<slug:slug>/unit_registration', views.available_units_for_registration, name='unit_registration'),

    path('attendance_request', views.AttendanceRequest.as_view(), name='attendance_request'),
    # path('mark_attendance', views.markAttendance, name='mark_attendance'),
    path('attendance/<slug:slug>', views.class_attendance, name='attendance'),


]
