import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """ A user manager for the user model with email as username"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email address must be provided'))
        if not password:
            raise ValueError(_('Password must be provided'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_satff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class StoreUser(AbstractUser):
    """ Custom user model to accept email as username"""
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)  # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    objects = UserManager()

    def __str__(self):
        return self.email


class CustomerUser(models.Model):
    """User Model for store customers"""
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, related_name='customeruser')

    def __str__(self):
        return self.user.email


class StoreAdminUser(models.Model):
    """User Model for store Admin"""
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, related_name='storeadmin')

    def __str__(self):
        return self.user.email

