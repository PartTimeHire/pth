from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.create_job_request, name='create_job_request'),
    path('job_search', views.job_search, name='job_search'),
]
