from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from attendance.models import AttendanceRecord
from timetable.models import Class
from accounts.models import UserProfile

class AttendanceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher', password='testpass123')
        self.student = User.objects.create_user(username='student', password='testpass123')
        UserProfile.objects.create(user=self.teacher, role='teacher')
        UserProfile.objects.create(user=self.student, role='student')
        self.class_obj = Class.objects.create(
            subject='Math',
            teacher=self.teacher,
            day='MON',
            start_time='09:00:00',
            end_time='10:00:00',
            room='101'
        )

    def test_generate_qr_code_view(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('generate_qr_code', args=[self.class_obj.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'QR Code for Attendance', html=True)

    def test_mark_attendance_view(self):
        self.client.login(username='student', password='testpass123')
        response = self.client.post(reverse('mark_attendance'), {'qr_data': f'{self.class_obj.id}:{timezone.now().timestamp()}'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Attendance marked successfully')

    def test_export_attendance_view(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('export_attendance', args=[self.class_obj.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename=attendance_{self.class_obj.id}.xlsx')

    def test_attendance_record_model(self):
        attendance_record = AttendanceRecord.objects.create(
            student=self.student,
            class_attended=self.class_obj,
            status='PRESENT'
        )
        self.assertEqual(attendance_record.student, self.student)
        self.assertEqual(attendance_record.class_attended, self.class_obj)
        self.assertEqual(attendance_record.status, 'PRESENT')