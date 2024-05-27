from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, UserProfile, Job, JobRequest, Message, Rating, Notification

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'bio', 'location')
    search_fields = ('user__username', 'bio', 'location')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'amount', 'progress', 'creator', 'created_at', 'deadline')
    search_fields = ('title', 'description', 'creator__username')
    list_filter = ('progress', 'categories', 'created_at', 'deadline')

@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'location', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_filter = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'related_to_active_job')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp', 'related_to_active_job')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'creator', 'job', 'comment', 'timestamp')
    search_fields = ('user__username', 'creator__username', 'job__title', 'comment')
    list_filter = ('rating', 'timestamp')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'read')
    search_fields = ('user__username', 'message')
    list_filter = ('timestamp', 'read')
