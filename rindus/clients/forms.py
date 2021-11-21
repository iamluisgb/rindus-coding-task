"""Client forms."""

# Django
from django import forms

# Models
from rindus.clients.models import Client


class ClientForm(forms.ModelForm):
    """Client model form."""

    class Meta:
        """Form settings."""

        model = Client
        fields = ('user', 'first_name', "last_name", "iban")