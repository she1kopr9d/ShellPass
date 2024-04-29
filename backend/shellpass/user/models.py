from enum import unique
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', default='media/profile/avatar.png')
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
