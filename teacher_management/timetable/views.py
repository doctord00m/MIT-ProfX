from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Class, TimetableChangeRequest, Notification
from .forms import TimetableChangeRequestForm

@login_required
def timetable_view(request):
    slots = [
        "9:00 AM - 9:50 AM",
        "9:50 AM - 10:40 AM",
        "BREAK",
        "10:50 AM - 11:40 AM",
        "11:40 AM - 12:30 PM",
        "BREAK",
        "1:00 PM - 1:50 PM",
        "1:50 PM - 2:40 PM",
        "BREAK",
        "2:50 PM - 3:40 PM",
        "3:40 PM - 4:30 PM"
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {day: {slot: None for slot in slots} for day in days}
    timetable = {day: {slot: None for slot in slots} for day in days}
    classes = Class.objects.all()
    for class_obj in classes:
        day = class_obj.get_day_display()
        start_time = class_obj.start_time.strftime("%I:%M %p")
        end_time = class_obj.end_time.strftime("%I:%M %p")
        slot = f"{start_time} - {end_time}"
        if slot in timetable[day]:
            timetable[day][slot] = class_obj
            timetable[day][slot] = class_obj
    return render(request, 'timetable/timetable.html', {'timetable': timetable, 'slots': slots, 'days': days})

@login_required
def update_timetable_view(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, "Only teachers can update the timetable.")
        return redirect('timetable_view')

    if request.method == 'POST':
        form = TimetableChangeRequestForm(request.POST)
        if form.is_valid():
            change_request = form.save(commit=False)
            change_request.requester = request.user
            change_request.save()
            # Create notification for all teachers
            teachers = User.objects.filter(userprofile__role='teacher')
            for teacher in teachers:
                Notification.objects.create(
                    user=teacher,
                    message=f"New timetable change request from {request.user.username}"
                )
            messages.success(request, "Timetable change request submitted successfully.")
            return redirect('timetable_view')
    else:
        form = TimetableChangeRequestForm()

    return render(request, 'timetable/update_timetable.html', {'form': form})

@login_required
def handle_change_request(request, request_id):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, "Only teachers can handle change requests.")
        return redirect('timetable_view')

    change_request = TimetableChangeRequest.objects.get(id=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            change_request.status = 'APPROVED'
            # Update the original class
            original_class = change_request.original_class
            original_class.day = change_request.proposed_day
            original_class.start_time = change_request.proposed_start_time
            original_class.end_time = change_request.proposed_end_time
            original_class.save()
            messages.success(request, "Change request approved and timetable updated.")
        elif action == 'deny':
            change_request.status = 'DENIED'
            messages.success(request, "Change request denied.")
        change_request.save()
    return redirect('timetable_view')

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'timetable/notifications.html', {'notifications': notifications})