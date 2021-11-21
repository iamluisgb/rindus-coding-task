"""Django models utilities."""

# Django
from django.db import models

class RBModel(models.Model):
    """ Rindus bank base model.

    RBMode acts as an abstract base class from which every 
    other model in the project will inheri . This class provides
    every table with the following attributes:
        + created (DateTime).
        + modified (DateTime).
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
        )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
        )

    class Meta:
        """Meta option. """

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
