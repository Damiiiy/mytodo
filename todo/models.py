from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# # Create your models here
 
class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True, null=True)
    password = models.CharField(max_length=255 , null =True)

    # USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Task(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'Completed' if self.completed else 'Pending'})"



   

# class Task(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     task_name = models.CharField(max_length=100, null=True)
#    
#     time_created = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False, null=True)

#     def __str__(self):
        # return self.task_name
