from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from .managers import CustomUserManager

import random


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["username", "email"]  # No additional required fields

    def __str__(self):
        return self.phone_number


class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        return (now() - self.created_at).total_seconds() < 300 
    
    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    province = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.province}, {self.city}"
    
    
    