from django.shortcuts import redirect

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.userprofile.role == 'student' and request.path.startswith('/teacher/'):
                return redirect('timetable_view')
            elif request.user.userprofile.role == 'teacher' and request.path.startswith('/student/'):
                return redirect('timetable_view')
        return self.get_response(request)