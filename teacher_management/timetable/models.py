from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetable_classes')
    day = models.CharField(max_length=10, choices=[
        ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
        ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.subject} - {self.teacher.username} - {self.day}"

class TimetableChangeRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='change_requests')
    original_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='change_requests')
    proposed_day = models.CharField(max_length=10, choices=Class.day.field.choices)
    proposed_start_time = models.TimeField()
    proposed_end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied')
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change request for {self.original_class} by {self.requester.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."