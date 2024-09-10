from django.urls import path
from . import views as account_views
from timetable import views as timetable_views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from calendar_events import views as calendar_views

urlpatterns = [
    path('', account_views.login_view, name='root'),
    path('login/', account_views.login_view, name='login'),
    path('student/login/', account_views.student_login_view, name='student_login'),
    path('teacher/login/', account_views.teacher_login_view, name='teacher_login'),
    path('register/', account_views.register_view, name='register'),
    path('verify-email/', account_views.verify_email, name='verify_email'),
    path('student/dashboard/', account_views.student_dashboard_view, name='student_dashboard'),
    path('teacher/dashboard/', account_views.teacher_dashboard_view, name='teacher_dashboard'),
    path('logout/', account_views.logout_view, name='logout'),
    path('timetable/', timetable_views.timetable_view, name='timetable_view'),
    path('calendar/', calendar_views.CalendarView.as_view(), name='calendar'),
    path('calendar/events/', calendar_views.get_events, name='get_events'),
    path('create/', calendar_views.create_event, name='create_event'),
]