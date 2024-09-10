from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Event, Subject
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

@method_decorator(login_required, name='dispatch')
class CalendarView(View):
    template_name = 'calendar_events/calendar.html'

    def get(self, request):
        subjects = Subject.objects.all()
        return render(request, self.template_name, {'subjects': subjects})

@login_required
@require_http_methods(["GET"])
def get_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    events = Event.objects.filter(start__gte=start, end__lte=end)
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat(),
            'extendedProps': {
                'subject': event.subject.id,
                'type': event.event_type,
                'notes': event.additional_notes,
            }
        })
    return JsonResponse(event_list, safe=False)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_event(request):
    data = json.loads(request.body)
    event = Event.objects.create(
        title=data['title'],
        start=parse_datetime(data['start']),
        end=parse_datetime(data['end']),
        subject_id=data['subject'],
        event_type=data['type'],
        additional_notes=data['notes'],
        teacher=request.user
    )
    return JsonResponse({
        'id': event.id,
        'title': event.title,
        'start': event.start.isoformat(),
        'end': event.end.isoformat(),
        'extendedProps': {
            'subject': event.subject.id,
            'type': event.event_type,
            'notes': event.additional_notes,
        }
    })

@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    data = json.loads(request.body)
    
    event.title = data['title']
    event.event_type = data['type']
    event.subject_id = data['subject']
    event.additional_notes = data['notes']
    event.start = parse_datetime(data['start'])
    event.end = parse_datetime(data['end'])
    event.save()

    return JsonResponse({
        'id': event.id,
        'title': event.title,
        'start': event.start.isoformat(),
        'end': event.end.isoformat(),
        'extendedProps': {
            'subject': event.subject.id,
            'type': event.event_type,
            'notes': event.additional_notes,
        }
    })

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return JsonResponse({'success': True})
