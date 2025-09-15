from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('lookup/', views.student_lookup, name='student_lookup'),
    path('save_result/', views.save_result, name='save_result'),
]