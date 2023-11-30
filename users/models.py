from django.db import models
from django.contrib.auth.models import User



# Create your models here.

# Create a new user

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"

