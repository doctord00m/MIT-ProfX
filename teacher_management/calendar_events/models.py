from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def create_default_subjects(cls):
        subjects = [
            "Information Security",
            "Principles of Operating Systems",
            "Essentials of Management",
            "Software Project Management",
            "Software Engineering",
            "Principles of Operating Systems Laboratory",
            "Information Security Laboratory",
            "Creativity, Problem Solving & Innovation"
        ]
        for subject_name in subjects:
            cls.objects.get_or_create(name=subject_name)

class Event(models.Model):
    EVENT_TYPES = [
        ('Lab Record Submission', 'Lab Record Submission'),
        ('Viva Voce & Record Submission', 'Viva Voce & Record Submission'),
        ('Lab midsem exam', 'Lab midsem exam'),
        ('Midsem Exam', 'Midsem Exam'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Test', 'Test'),
    ]

    title = models.CharField(max_length=200, default="Untitled Event")
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)  # Assumes Subject with id=1 exists
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='Assignment')
    additional_notes = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Assumes User with id=1 exists

    def __str__(self):
        return f"{self.title} - {self.subject}"
