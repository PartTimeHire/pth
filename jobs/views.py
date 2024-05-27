from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobRequestForm
from .models import JobRequest

@login_required
def create_job_request(request):
    if request.method == 'POST':
        form = JobRequestForm(request.POST)
        if form.is_valid():
            job_request = form.save(commit=False)
            job_request.posted_by = request.user
            job_request.save()
            return redirect('job_list')
    else:
        form = JobRequestForm()
    return render(request, 'create_job_request.html', {'form': form})

def job_list(request):
    jobs = JobRequest.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

def job_search(request):
    query = request.GET.get('q')
    jobs = JobRequest.objects.filter(title__icontains=query) if query else JobRequest.objects.all()
    return render(request, 'job_search.html', {'jobs': jobs})
