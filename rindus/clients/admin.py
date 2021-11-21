"""Clients  model admin."""

# Django
from django.contrib import admin

# Models
from rindus.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Client admin."""

    list_display = ('id', 'user', 'first_name', 'last_name', 'iban')
    list_filter = ('created', 'modified')
