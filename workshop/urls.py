from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/logo.svg'))),
    # Frontend Public Routes
    path('', views.home_view, name='home'),
    path('courses/', views.courses_list_view, name='courses_list'),
    path('courses/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('register/', views.registration_view, name='registration'),
    path('registration-success/<str:reg_id>/', views.registration_success_view, name='registration_success'),

    # Custom Admin Authentication Routes
    path('custom-admin/login/', views.admin_login_view, name='admin_login'),
    path('custom-admin/logout/', views.admin_logout_view, name='admin_logout'),

    # Custom Admin Dashboard Routes
    path('custom-admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('custom-admin/registrations/', views.admin_registrations_list_view, name='admin_registrations_list'),
    path('custom-admin/registrations/export/', views.admin_export_registrations_csv, name='admin_registrations_export'),
    path('custom-admin/registrations/import/', views.admin_import_registrations_csv, name='admin_registrations_import'),
    path('custom-admin/registrations/<str:reg_id>/', views.admin_registration_detail_view, name='admin_registration_detail'),
    path('custom-admin/registrations/<str:reg_id>/status/', views.admin_update_registration_status_view, name='admin_update_status'),
    path('custom-admin/registrations/<str:reg_id>/delete/', views.admin_delete_registration_view, name='admin_delete_registration'),
    path('custom-admin/courses/', views.admin_courses_list_view, name='admin_courses_list'),
    path('custom-admin/courses/<int:course_id>/', views.admin_course_edit_view, name='admin_course_edit'),
    path('custom-admin/events/', views.admin_events_list_view, name='admin_events_list'),
    path('custom-admin/events/add/', views.admin_event_edit_view, name='admin_event_add'),
    path('custom-admin/events/<int:event_id>/', views.admin_event_edit_view, name='admin_event_edit'),
    path('custom-admin/settings/', views.admin_settings_edit_view, name='admin_settings_edit'),
    path('custom-admin/change-credentials/', views.admin_change_credentials_view, name='admin_change_credentials'),

    # Attendance & Computer Vision Routes
    path('custom-admin/attendance/', views.admin_attendance_view, name='admin_attendance'),
    path('custom-admin/attendance/scan-api/', views.admin_attendance_scan_api, name='admin_attendance_scan_api'),
    path('custom-admin/attendance/summary/', views.admin_attendance_summary_view, name='admin_attendance_summary'),
    path('custom-admin/attendance/export/', views.admin_export_attendance_csv, name='admin_attendance_export'),

    # Student Feedback Routes
    path('feedback/', views.feedback_view, name='feedback'),
    path('custom-admin/feedback/', views.admin_feedback_list_view, name='admin_feedback_list'),
    path('custom-admin/feedback/<int:feedback_id>/delete/', views.admin_delete_feedback_view, name='admin_delete_feedback'),
    path('custom-admin/feedback/export/', views.admin_export_feedback_csv, name='admin_feedback_export'),
]
