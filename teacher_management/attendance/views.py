import qrcode
import base64
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import AttendanceRecord
from timetable.models import Class
import pandas as pd

@login_required
def generate_qr_code(request, class_id):
    if request.user.userprofile.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    class_obj = Class.objects.get(id=class_id)
    timestamp = timezone.now().timestamp()
    qr_data = f"{class_id}:{timestamp}"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'attendance/generate_qr.html', {'qr_image': img_str})

@login_required
def mark_attendance(request):
    if request.user.userprofile.role != 'student':
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        class_id, timestamp = qr_data.split(':')
        
        # Check if the QR code is not older than 2 seconds
        if float(timestamp) + 2 < timezone.now().timestamp():
            return HttpResponse("QR code expired", status=400)

        class_obj = Class.objects.get(id=class_id)
        AttendanceRecord.objects.create(
            student=request.user,
            class_attended=class_obj,
            status='PRESENT'
        )
        return HttpResponse("Attendance marked successfully")

    return render(request, 'attendance/scan_qr.html')

@login_required
def export_attendance(request, class_id):
    if request.user.userprofile.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    class_obj = Class.objects.get(id=class_id)
    attendance_records = AttendanceRecord.objects.filter(class_attended=class_obj)
    data = list(attendance_records.values_list('student__username', 'date', 'status'))
    df = pd.DataFrame(data, columns=['Student', 'Date', 'Status']) if data else pd.DataFrame(columns=['Student', 'Date', 'Status'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=attendance_{class_id}.xlsx'
    df.to_excel(response, index=False)
    return response