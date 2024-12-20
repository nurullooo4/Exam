from django.contrib.auth.models import AbstractUser
from django.db import models

from app_users.managers import UserModelManager, CustomerManager, AdminManager



class UserModel(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    EMAIL_FIELD = 'email'
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    user_image = models.ImageField(upload_to='user-images/',
                                   default='user-images/user-default.png',
                                   null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    objects = UserModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        ordering = ['id']


class Admin(UserModel):
    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_customer = False
        self.is_admin = True
        self.is_staff = True
        self.is_superuser = True
        super().save(*args, **kwargs)


class Customer(UserModel):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_customer = True
        self.is_admin = False
        self.is_staff = False
        self.is_superuser = False
        super().save(*args, **kwargs)


class Checkout(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    products = models.ManyToManyField('app_main.Product', related_name='checkout')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
