from django.db import models
from django.contrib.auth.models import User
from datetime import time
from PIL import Image

# Create your models here.

SIZE_CHOICES = (
    ("Small | £50", "small | £50"),
    ("Normal | £80", "normal | £80"),
    ("Large | £100", "large | £100"),
    ("Extra-Large | £120", "extra-large | £120"),
)

LENGTH_CHOICES = (
    ("Bra", "bra"),
    ("Mid-Back", "mid-back"),
    ("Waist", "waist"),
    ("Butt", "butt"),
    ("Mid Thighs", "mid thighs"),
    ("Knees", "knees"),
)

def default_image_path():
    return 'hairstyle4.jpg'

class Hairstyles(models.Model):
    title = models.CharField(max_length=200, null=False)
    time = models.FloatField(null=False)
    image = models.ImageField(default=default_image_path, upload_to='hairstyle_pics')
    description = models.TextField(null=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"




# Generate hour choices from 9 AM to 9 PM with 1-hour increments

TIME_CHOICES = [(time(hour, 0), f'{hour:02d}:00') for hour in range(9, 18)]


class Appointment(models.Model):
    title = models.ForeignKey(Hairstyles, on_delete=models.CASCADE, related_name='appointment_name', default=Hairstyles)
    date = models.DateField()
    time = models.TimeField(choices=TIME_CHOICES, default=TIME_CHOICES[3][0])
    size_and_price = models.CharField(max_length=100, choices=SIZE_CHOICES, default=SIZE_CHOICES[1][0])
    length = models.CharField(max_length=100, choices=LENGTH_CHOICES, default=LENGTH_CHOICES[0][0])
    is_confirmed = models.BooleanField(default=False)
    client_name = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.client_name}'s {self.title} Appointment on {self.date} at {self.time}"


class ContactUs(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    client_message = models.TextField(null=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}'s message"
