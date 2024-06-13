from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class MdbUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    ROLE_CHOICES = (
        (USER, _('User')),
        (MODERATOR, _('Moderator')),
        (ADMIN, _('Admin')),
    )
    role = models.CharField(_('role'), max_length=10, choices=ROLE_CHOICES,
                            default=USER)

    class Meta:
        ordering = ['id']
