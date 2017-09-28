from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class user_info(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    is_verified = models.BooleanField()
    token = models.IntegerField()

    def __str__(self):
        return self.email