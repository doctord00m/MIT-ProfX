from django.db import models
from django.contrib.auth.models import User
from timetable.models import Class

class AttendanceRecord(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent')])

    class Meta:
        unique_together = ('student', 'class_attended', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.class_attended} - {self.date}"