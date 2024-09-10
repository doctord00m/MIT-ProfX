from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

def student_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.userprofile.role == 'student':
                login(request, user)
                return redirect('timetable_view')
            else:
                form.add_error(None, "Invalid username or password for student.")
    else:
        form = LoginForm()
    return render(request, 'accounts/student_login.html', {'form': form})

def teacher_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.userprofile.role == 'teacher':
                login(request, user)
                return redirect('timetable_view')
            else:
                form.add_error(None, "Invalid username or password for teacher.")
    else:
        form = LoginForm()
    return render(request, 'accounts/teacher_login.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.user
        if user.userprofile.verification_code == code:
            user.userprofile.email_verified = True
            user.userprofile.save()
            return redirect('dashboard')  # Redirect to appropriate dashboard
        else:
            return render(request, 'verify_email.html', {'error': 'Invalid code'})
    return render(request, 'verify_email.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('timetable_view')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def student_dashboard_view(request):
    return render(request, 'student_dashboard.html')

def teacher_dashboard_view(request):
    return render(request, 'teacher_dashboard.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('timetable_view')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('timetable_view')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')