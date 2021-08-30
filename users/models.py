from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from users.managers import CustomUserManager

class Department(models.Model):
    department = models.CharField(max_length=40, null=False)

    def __str__(self):
        return self.department
        
class User(AbstractBaseUser, PermissionsMixin):
   full_name = models.CharField(max_length=60, null=False)
   password = models.CharField(max_length=300, null=False)
   is_staff = models.BooleanField(default=False)
   is_active = models.BooleanField(default=True)
   email = models.EmailField(max_length=60, null=False, unique=True)
   department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['full_name', 'password']

   objects = CustomUserManager()

   def __str__(self):
       return self.email