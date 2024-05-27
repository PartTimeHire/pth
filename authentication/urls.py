from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home_authenticated/', views.home_authenticated, name='home_authenticated'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_job_request/', views.create_job_request, name='create_job_request'),
    path('job_search/', views.job_search, name='job_search'),
]
