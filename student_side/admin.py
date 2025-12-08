from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import StudentProfile, Task


def export_selected_profiles(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="selected_profiles.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Student ID",
        "Commitment",
        "Experience level",
        "Lead preference",
        "Tasks",
    ])

    for p in queryset:
        writer.writerow([
            p.student_id,
            p.commitment,
            p.experience_level,
            p.lead_preference,
            ", ".join(t.name for t in p.preferred_tasks.all()),
        ])

    return response

export_selected_profiles.short_description = "Download selected profiles (CSV)"


def export_all_profiles(modeladmin, request, queryset):
    queryset = StudentProfile.objects.all()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="all_profiles.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Student ID",
        "Commitment",
        "Experience level",
        "Lead preference",
        "Tasks",
    ])

    for p in queryset:
        writer.writerow([
            p.student_id,
            p.commitment,
            p.experience_level,
            p.lead_preference,
            ", ".join(t.name for t in p.preferred_tasks.all()),
        ])

    return response

export_all_profiles.short_description = "Download ALL profiles (CSV)"


def clear_all_profiles(modeladmin, request, queryset):
    StudentProfile.objects.all().delete()

clear_all_profiles.short_description = "Delete ALL profiles"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student_id", "commitment", "experience_level", "lead_preference")
    actions = [
        "export_selected_profiles",
        "export_all_profiles",
        "clear_all_profiles",
    ]


def clear_all_tasks(modeladmin, request, queryset):
    Task.objects.all().delete()

clear_all_tasks.short_description = "Delete ALL tasks"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    actions = ["clear_all_tasks"]