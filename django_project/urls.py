from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create-job/', views.create_job, name='create_job'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-job-request/', views.create_job_request, name='create_job_request'),
    path('job-search/', views.job_search, name='job_search'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),  # Ensure this line points to the correct function
    path('logout/', views.logout, name='logout'),
    path('email-verification/', views.verify_email, name='email_verification'),
    path('home-authenticated/', views.home_authenticated, name='home_authenticated'),
    path('auth/', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),
]
