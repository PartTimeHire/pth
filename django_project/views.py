from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import JobRequest
from .forms import JobRequestForm, ProfileEditForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return redirect('home_authenticated')
    return render(request, 'home.html')

@login_required
def home_authenticated(request):
    return render(request, 'home_authenticated.html')

def about(request):
    return render(request, 'about.html')

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Job created successfully!")
    else:
        form = JobRequestForm()
    return render(request, 'create_job.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileEditForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_job_request(request):
    if request.method == 'POST':
        form = JobRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_authenticated.html')
    else:
        form = JobRequestForm()
    return render(request, 'create_job_request.html', {'form': form})

def job_search(request):
    job_requests = JobRequest.objects.all()
    return render(request, 'job_search.html', {'job_requests': job_requests})

def redirect_to_signup_or_login(request):
    return render(request, 'choose_signup_or_login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            verification_code = form.send_verification_email()  # Send verification email
            request.session['user_data'] = user_data
            request.session['verification_code'] = verification_code
            return redirect('email_verification')
        else:
            messages.error(request, 'Error processing your request. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_authenticated')
        else:
            # Handle invalid login credentials
            return HttpResponse("Invalid username or password.")
    else:
        # Handle GET request for login page
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        stored_verification_code = request.session.get('verification_code')
        if verification_code == stored_verification_code:
            user_data = request.session.get('user_data')
            if user_data:
                user = User.objects.create_user(**user_data)
                user.is_active = True
                user.save()
                del request.session['user_data']
                del request.session['verification_code']
                auth_login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid verification code. Please try again.")
    return render(request, 'email_verification.html')
