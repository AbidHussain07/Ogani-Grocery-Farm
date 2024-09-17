from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# For Admin Log In ------->
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=30)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self) -> str:
        return self.username