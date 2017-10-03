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
    register_date = models.DateTimeField(null=True)
    expiry_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.email

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s" % (filename)

def get_gallery_file_name(instance, filename):
    return "gallery_%s" % (filename)

class donate_info(models.Model):
    request_id = models.AutoField(primary_key=True)
    is_resolved = models.BooleanField()
    user_name = models.CharField(max_length=100)
    request_date = models.DateField(null=True)
    food_image = models.FileField(null=True, upload_to=get_upload_file_name)
    latitude = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.request_id)

class food_info(models.Model):
    food_id = models.AutoField(primary_key=True)
    request_id = models.CharField(max_length=100, null=True)
    user_name = models.CharField(max_length=100)
    food_name = models.CharField(max_length=100, null=True)
    item_amount = models.CharField(max_length=100, null=True)
    expiry_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.food_name
class gallery_info(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to=get_gallery_file_name)

    def __str__(self):
        return str(self.image_id)
