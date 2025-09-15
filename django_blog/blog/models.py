from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=50, unique=True)
    series = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.register_number})"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    subject = models.CharField(max_length=100)
    s1 = models.FloatField(default=0)
    s2 = models.FloatField(default=0)
    sem = models.FloatField(default=0)
    lab = models.FloatField(default=0)
    marks = models.FloatField(default=0)
    grade = models.CharField(max_length=5)
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
