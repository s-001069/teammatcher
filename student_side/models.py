from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class StudentProfile(models.Model):
    student_id = models.CharField(max_length=200)

    availability_monday = models.CharField(max_length=200, blank=True)
    availability_tuesday = models.CharField(max_length=200, blank=True)
    availability_wednesday = models.CharField(max_length=200, blank=True)
    availability_thursday = models.CharField(max_length=200, blank=True)
    availability_friday = models.CharField(max_length=200, blank=True)
    availability_saturday = models.CharField(max_length=200, blank=True)
    availability_sunday = models.CharField(max_length=200, blank=True)

    commitment = models.CharField(max_length=20, blank=True)
    educational_background = models.CharField(max_length=200, blank=True)
    professional_background = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    experience_level = models.CharField(max_length=20, blank=True)
    lead_preference = models.CharField(max_length=20, blank=True)
    preferred_tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.student_id
