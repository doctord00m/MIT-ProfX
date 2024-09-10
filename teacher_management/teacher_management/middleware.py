from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path not in [reverse('login'), reverse('register')] and not request.path.startswith('/admin/'):
                return redirect('login')
        else:
            if request.path in ['/', reverse('login'), reverse('register')]:
                return redirect('timetable_view')
        return self.get_response(request)