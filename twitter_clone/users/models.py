from django.contrib.auth.models import AbstractUser, UserManager as BaseManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_me_word


class UserManager(BaseManager):
    def follow_toggle(self, user, follower):
        if follower in user.followers.all():
            is_following = False
            user.followers.remove(follower)
        else:
            is_following = True
            user.followers.add(follower)
        return is_following


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator, validate_me_word],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(
        _('Name of User'), null=True, blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    followers = models.ManyToManyField("self", blank=True)
    objects = UserManager()

    def get_absolute_url(self):
        return reverse('api:user-detail', kwargs={'username': self.username})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Other Details')
    picture = models.ImageField(_('Profile picture'), upload_to='profile_pictures', null=True, blank=True)
    bio = models.TextField(_('Biography'), null=True, blank=True, max_length=2048)
    website = models.URLField(_('Website'), null=True, blank=True)
    phone = models.CharField(_('Phone Number'), max_length=11, blank=True)
    address = models.CharField(_('Address'), max_length=100, blank=True)

    def __str__(self):
        return ''


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ Create a profile anytime a new user is created """
    if kwargs['created']:
        user_profile = UserProfile.objects.get_or_create(
            user=kwargs['instance']
        )
