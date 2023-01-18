import uuid as uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from model_utils import Choices
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import  AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

class BaseModel(models.Model):
    """
    Define base model to frequent use
    """
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    password = models.CharField(max_length=1024)
    email = models.EmailField(max_length=128, unique=True)
    name = models.CharField(max_length=1024, null=True,blank=True)
    contact = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024, null=True,blank=True)
    city =models.CharField(max_length=1024, null=True,blank=True)
    pincode = models.CharField(max_length=1024, null=True,blank=True)
    state=models.CharField(max_length=1024, null=True,blank=True)
    country = models.CharField(max_length=1024,default='India', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    is_register = models.BooleanField(default=False)
    access_counter = models.IntegerField(default=0)
    access_timer = models.DateTimeField(auto_now_add=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_associated_team(self):
        return self.rel_manage_team_user.all()


class Otp(BaseModel):
    is_active = None
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='rel_user_otp')
    otp = models.CharField(max_length=6, blank=True, null=True, default=0)
    is_used = models.BooleanField(default=False)