"""User admin classes."""

# Django
from django.contrib.auth.admin import UserAdmin 
from django.contrib import admin

# Models
from django.contrib.auth.models import User
from rindus.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin. """

    list_display = ('username','email', 'first_name', 'last_name')
    list_filter = ('created', 'modified')
    list_editable = ('email', 'first_name', 'last_name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('biography', 'picture')

admin.site.register(User, CustomUserAdmin)