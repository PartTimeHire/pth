from django import forms
from .models import JobRequest

class JobRequestForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = ['title', 'description']
