from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(
        _('Name of User'), null=True, blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    bio = models.CharField(_('Biography'), null=True,
                           blank=True, max_length=255)
    website = models.URLField(_('Website'), null=True, blank=True)
    # folowers = models.ManyToManyField('self', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('api:user-detail', kwargs={'username': self.username})
