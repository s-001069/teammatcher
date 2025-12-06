from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("student/", include(("student_side.urls", "student_side"), namespace="student_side")),
    path("teacher/", include(("teacher_side.urls", "teacher_side"), namespace="teacher_side")),
]