from django.contrib import admin
from .models import Student, Result

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'register_number', 'series')
    search_fields = ('name', 'register_number')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'grade', 'status')
    list_filter = ('student', 'subject', 'grade', 'status')
