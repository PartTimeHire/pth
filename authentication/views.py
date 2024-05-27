# AUTHENTICATION/VIEWS.PY
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def home(request):
    if request.user.is_authenticated:
        return redirect('home_authenticated')
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        user = User(username=username, email=email, first_name=firstname, last_name=lastname)
        user.set_password(password1)
        user.is_active = False
        user.save()

        send_verification_email(request, user)
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address to activate your account.")

        return redirect('login')

    return render(request, "signup.html")


def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your PartTimeHire Account'
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    # Debugging logs
    logger.debug(f'uidb64: {uidb64}, token: {token}')
    print(f'uidb64: {uidb64}, token: {token}')  # Debug print

    protocol = 'https' if request.is_secure() else 'http'
    domain = current_site.domain
    port = request.get_port()
    
    # Construct the full URL with the port if it's a development environment
    if port and port != '80':
        domain = f"{domain}:{port}"

    context = {
        'name': user.first_name,
        'domain': domain,
        'uid': uidb64,
        'token': token,
        'protocol': protocol,
    }
    message = render_to_string('email_verification.html', context)
    print(message)  # Debug: print the rendered HTML content
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.content_subtype = "html"  # Set the email content to HTML
    email.send(fail_silently=True)




@csrf_exempt
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect('home_authenticated')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('home')


def activate_view(request, uidb64, token):
    return render(request, 'activate.html', {'uidb64': uidb64, 'token': token})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home_authenticated')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def home_authenticated(request):
    return render(request, 'home_authenticated.html')

@login_required
def edit_profile(request):
    return render(request, 'edit_profile.html')

@login_required
def create_job_request(request):
    return render(request, 'create_job_request.html')

@login_required
def job_search(request):
    return render(request, 'job_search.html')
