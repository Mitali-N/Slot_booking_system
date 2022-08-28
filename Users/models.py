from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
        username = models.ForeignKey(User, on_delete=models.CASCADE)   


class Staff(models.Model):
        username = models.ForeignKey(User, on_delete=models.CASCADE)                 
