from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable_view'),
    path('update/', views.update_timetable_view, name='update_timetable'),
    path('handle-request/<int:request_id>/', views.handle_change_request, name='handle_change_request'),
    path('notifications/', views.notifications_view, name='notifications'),
]