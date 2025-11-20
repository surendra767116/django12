from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/callback/', views.auth_callback, name='auth_callback'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('download/<str:file_id>/', views.download_pdf, name='download_pdf'),
    path('delete/<str:file_id>/', views.delete_pdf, name='delete_pdf'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/upload/', views.admin_upload_pdf, name='admin_upload_pdf'),
]
