from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import LoginForm

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='student', password='testpass123')
        self.teacher = User.objects.create_user(username='teacher', password='testpass123')
        UserProfile.objects.create(user=self.student, role='student')
        UserProfile.objects.create(user=self.teacher, role='teacher')

    def test_student_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'student', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('timetable_view'))

    def test_teacher_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'teacher', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('timetable_view'))

    def test_login_form(self):
        form_data = {'username': 'testuser', 'password': 'testpass123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_model(self):
        student_profile = UserProfile.objects.get(user=self.student)
        self.assertEqual(student_profile.role, 'student')
        teacher_profile = UserProfile.objects.get(user=self.teacher)
        self.assertEqual(teacher_profile.role, 'teacher')