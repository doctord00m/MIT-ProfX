from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile
from .models import Event
from django.utils import timezone
from django.utils import timezone
from .models import Event, Subject

class CalendarViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher', password='testpass123')
        self.student = User.objects.create_user(username='student', password='testpass123')
        UserProfile.objects.create(user=self.teacher, role='teacher')
        UserProfile.objects.create(user=self.student, role='student')
        self.subject = Subject.objects.create(name='Test Subject')

    def test_calendar_view_authenticated(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_events/calendar.html')

    def test_calendar_view_unauthenticated(self):
        response = self.client.get(reverse('calendar'))
        expected_url = reverse('login')
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_event_create_view_teacher(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_events/event_form.html')

    def test_event_create_view_student(self):
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Only teachers can create events.", status_code=403)

    def test_create_event(self):
        self.client.login(username='teacher', password='testpass123')
        event_data = {
            'title': 'Test Event',
            'description': 'This is a test event',
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(hours=1),
        }
        response = self.client.post(reverse('event_create'), data=event_data)
        self.assertRedirects(response, reverse('calendar'))
        self.assertEqual(Event.objects.count(), 1)

class EventTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher', password='testpass123')
        self.student = User.objects.create_user(username='student', password='testpass123')
        UserProfile.objects.create(user=self.teacher, role='teacher')
        UserProfile.objects.create(user=self.student, role='student')
        self.subject = Subject.objects.create(name='Test Subject')

    def test_event_create_view_teacher(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 200)

    def test_event_create_view_student(self):
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 403)

    def test_create_event(self):
        self.client.login(username='teacher', password='testpass123')
        event_data = {
            'title': 'Test Event',
            'event_type': 'ASSIGNMENT',
            'subject': self.subject.id,
            'description': 'This is a test event',
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(hours=1),
        }
        response = self.client.post(reverse('event_create'), data=event_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(Event.objects.count(), 1)

    def test_event_detail(self):
        event = Event.objects.create(
            title='Test Event',
            event_type='EXAM',
            subject=self.subject,
            description='Test description',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            created_by=self.teacher
        )
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('event_detail', args=[event.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Test Event')
        self.assertEqual(data['type'], 'EXAM')
