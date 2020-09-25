from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('users must have an username')
        if not password:
            raise ValueError('User must have an password')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #   admin
    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    #   seller / merchant
    def create_staffuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_staff = False
        user.is_superuser = False
        user.is_active = False
        user.save(using=self._db)
        return user

    #   customer
    def create_activeuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return True


class MerchantAccount(models.Model):
    full_name = models.CharField(max_length=50)
    shop_name = models.CharField(max_length=50, blank=True)
    email = models.OneToOneField(UserAccount, on_delete=models.PROTECT)
    phone_num = models.PositiveIntegerField(unique=True)
    phone_num2 = models.PositiveIntegerField()
    aadhar = models.CharField(unique=True, max_length=16, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    pincode = models.PositiveSmallIntegerField(default=00)
    shop_established_date = models.DateField(blank=True, null=True)
    about_shop = models.CharField(max_length=200, blank=True)
    shop_img = models.ImageField(upload_to='ShopsIMG', blank=True)
    shop_type = models.CharField(max_length=15, default='Retailer')
    gst_num = models.CharField(max_length=15, blank=True)
    available_services = models.CharField(max_length=200, blank=True)
    average_price = models.PositiveIntegerField(default=00)

    EMAIL_FIELD = 'email'
    objects = AccountManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return True


class Message(models.Model):
    sender = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['timestamp']
