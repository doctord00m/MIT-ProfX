from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('teacher', 'Teacher'), ('student', 'Student')])
    email_verified = models.BooleanField(default=False)
