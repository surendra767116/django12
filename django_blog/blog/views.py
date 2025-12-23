from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Student, Result

# 1️⃣ Homepage / Calculator Page
def home(request):
    return render(request, "blog/home.html")


# 2️⃣ Save Results via AJAX POST
@csrf_exempt
def save_result(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data["name"]
            register_number = data["registerNumber"]
            series = data["series"]
            results = data["results"]

            # Get or create student
            student, created = Student.objects.get_or_create(
                register_number=register_number,
                defaults={"name": name, "series": series}
            )
            if not created:
                # Update existing student
                student.name = name
                student.series = series
                student.save()

            # Save each subject result
            for r in results:
                Result.objects.update_or_create(
                    student=student,
                    subject=r["subject"],
                    defaults={
                        "s1": r["s1"],
                        "s2": r["s2"],
                        "sem": r["sem"],
                        "lab": r["lab"],
                        "marks": r["marks"],
                        "grade": r["grade"],
                        "status": r["status"]
                    }
                )

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# 3️⃣ Student List Page
def student_list(request):
    students = Student.objects.all()
    return render(request, "blog/student_list.html", {"students": students})


# 4️⃣ Student Detail Page
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = student.results.all()
    return render(request, "blog/student_detail.html", {"student": student, "results": results})


# 5️⃣ Student Lookup by Register Number
def student_lookup(request):
    student = None
    query = request.GET.get("register_number")
    if query:
        student = Student.objects.filter(register_number=query).first()
    return render(request, "blog/student_lookup.html", {"student": student, "query": query})
