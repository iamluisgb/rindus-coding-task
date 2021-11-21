"""Posts models."""

# Django
from django.db import models
from django.conf import settings 
from django.core.validators import RegexValidator

# Utilities
from rindus.utils.models import RBModel

class Client(RBModel):
    """Client model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    iban = models.CharField(
        validators=[RegexValidator(regex='^([A-Z]{2}[ \\-]?[0-9]{2})(?=(?:[ \\-]?[A-Z0-9]){9,30}$)((?:[ \\-]?[A-Z0-9]{3,5}){2,7})([ \\-]?[A-Z0-9]{1,3})?$', 
        message='Invalid IBAN. Please use CAPITAL LETTERS.', code='nomatch')],
        max_length=32, blank=True)

    def __str__(self):
        """Return first name and user name."""
        return '{} by @{}'.format(self.first_name, self.user.username)
