from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from .consts import *
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
        Custom user model manager
        """

    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given username and password.
        """

        # This makes sure we got everything ready for the user
        if not username:
            raise ValueError(_(self.NO_VALUE_ERROR_MESSAGE.format('Username')))
        if not password:
            raise ValueError(_(self.NO_VALUE_ERROR_MESSAGE.format('Password')))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # preventing circular import error
    messages = models.ManyToManyField("api.Message", blank=True)
