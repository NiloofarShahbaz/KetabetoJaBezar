from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
    bio=models.TextField(max_length=500,blank=True,default='hello!this is my bio!')

