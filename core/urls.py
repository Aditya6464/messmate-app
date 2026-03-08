"""
URL configuration for core app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, admin_views

urlpatterns = [
    # Customer URLs
    path('', views.CustomerIDEntryView.as_view(), name='customer_id_entry'),
    path('attendance/<str:customer_id>/', views.MarkAttendanceView.as_view(), name='mark_attendance'),
    path('history/<str:customer_id>/', views.AttendanceHistoryView.as_view(), name='attendance_history'),
    
    # Admin Authentication
    path('admin/login/', auth_views.LoginView.as_view(template_name='admin_panel/login.html'), name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(), name='admin_logout'),
    
    # Admin Dashboard
    path('admin/dashboard/', admin_views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # Admin Customer Management
    path('admin/customers/', admin_views.CustomerListView.as_view(), name='admin_customer_list'),
    path('admin/customers/create/', admin_views.CustomerCreateView.as_view(), name='admin_customer_create'),
    path('admin/customers/<int:pk>/edit/', admin_views.CustomerEditView.as_view(), name='admin_customer_edit'),
    path('admin/customers/<int:pk>/delete/', admin_views.CustomerDeleteView.as_view(), name='admin_customer_delete'),
    
    # Admin QR & WhatsApp
    path('admin/customers/<int:pk>/qr/', admin_views.GenerateQRView.as_view(), name='admin_generate_qr'),
    path('admin/customers/<int:pk>/send-qr/', admin_views.SendQRWhatsAppView.as_view(), name='admin_send_qr'),
    
    # Admin Reports
    path('admin/reports/', admin_views.AttendanceReportView.as_view(), name='admin_attendance_report'),
    path('admin/reports/export/', admin_views.ExportAttendanceCSVView.as_view(), name='admin_export_csv'),
]
