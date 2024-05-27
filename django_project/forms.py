import random
import string
import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import JobRequest, UserProfile, Job, Message, Rating
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254, help_text='Please enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email
    
    def send_verification_email(self):
        print("Sending verification email...")  # Print statement for debugging
        email = self.cleaned_data['email']
        verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        try:
            send_mail(
                'Verification Code',
                render_to_string('email_verification.html', {'verification_code': verification_code}),
                'jaddjamesjd@gmail.com',  # Replace with your email address
                [email],
                fail_silently=False,
            )
            print("Verification email sent to:", email)  # Print statement for debugging
            return verification_code
        except Exception as e:
            print("Error sending verification email:", str(e))
            return None

class JobRequestForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = ['title', 'description', 'price', 'location']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'amount', 'progress', 'categories', 'creator', 'deadline']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content', 'related_to_active_job']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
