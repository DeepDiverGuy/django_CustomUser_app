import uuid
import re

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser


# Create your MODELS here.



def validate_gmail(value):
    # GMAIL validation logic; 
    if re.split('@', value)[-1] != 'gmail.com':
        raise ValidationError(
            _('%(value)s is NOT a valid GMAIL account. Only Gmail address is allowed'),
            params={'value': value},
        )



class user(AbstractUser):

    """
    A fully featured Custom User Model with admin-compliant permissions. 
    Email and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    uuid_value = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False,
        null=False)
    email = models.EmailField(
        _('email address'), 
        unique=True, 
        blank=False, 
        null=False, )
    temp_email = models.EmailField(
        _('Temporary email address'), 
        blank=True, 
        null=True, )
    username = models.CharField(
        _('username'), 
        max_length=150, 
        unique=True, 
        blank=True, 
        null=True, 
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'), 
        validators=[username_validator], 
        error_messages={'unique': _("A user with that username already exists.")})
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ))

    # Other Fields can be included according to project's needs

    def get_absolute_url(self):
        return reverse('CustomUser:profile', kwargs={'uuid_value': self.uuid_value})

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = ['username']

    class Meta:
        abstract = False


