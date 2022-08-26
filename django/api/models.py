from django.db import models
from django.conf import settings
from django.contrib.auth.models import User as DefaultUser

from django.db.models.signals import post_save
from django.dispatch import receiver


from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone # fix erorr "global name 'timezone' is not defined"

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password):
        '''Create and save a user with the given email, and password.'''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password)

    def create_superuser(self, email, password):
        return self._create_user(email, password)

from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, max_length=255, blank=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Add additional fields here if needed

    objects = UserManager()

    USERNAME_FIELD = 'email'



