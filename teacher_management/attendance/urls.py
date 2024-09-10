from django.urls import path
from . import views

urlpatterns = [
    path('generate-qr/<int:class_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('export/<int:class_id>/', views.export_attendance, name='export_attendance'),
]