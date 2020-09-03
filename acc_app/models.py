from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = False
        user.is_superuser = False
        user.is_both = False
        user.is_active = False
        user.is_first_login = False
        user.save(using=self._db)
        return user

    def create_activeuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_both = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
