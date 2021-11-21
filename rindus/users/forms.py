"""User forms."""

# Django
from django import forms

# Models
from rindus.users.models import User


class SignupForm(forms.Form):
    """Sign up form."""

    username = forms.CharField(min_length=4, max_length=50,
        widget=forms.TextInput(
        attrs={
            'class': 'input-material',
            'placeholder': 'Nombre de usuario',
        }))

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(
        attrs={
            'class': 'input-material',
            'placeholder': 'Contraseña',
        }))
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(
        attrs={
            'class': 'input-material',
            'placeholder': 'Confirmación contraseña',
        }))

    first_name = forms.CharField(min_length=2, max_length=50,
        widget=forms.TextInput(
        attrs={
            'class': 'input-material',
            'placeholder': 'Nombre',
        }))

    last_name = forms.CharField(min_length=2, max_length=50,
        widget=forms.TextInput(
        attrs={
            'class': 'input-material',
            'placeholder': 'Apellidos',
        }))

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(
        attrs={
            'class': 'input-material',
            'placeholder': 'email',
        }))

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('El nombre de usuario ya existe')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden')

        return data

    def save(self):
        """Create user"""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)