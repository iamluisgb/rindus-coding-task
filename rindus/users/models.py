""""User model. """

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from rindus.utils.models import RBModel


class User(RBModel, AbstractUser):
    """User model.

    Extend from Django´s Abstract User, change the username field
    to email.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    def __str__(self):
        """Return username. """
        return self.username

    def get_short_name(self):
        """Return username. """
        return self.username

class Profile(RBModel):
    """Profile model.

    A profile holds a user's public data like biography and picture.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    biography = models.TextField(blank=True)
