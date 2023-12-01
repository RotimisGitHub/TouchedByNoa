from django.db import models
from django.contrib.auth.models import User
from datetime import time
from config.storage_backends import MediaStorage

# Create your models here.

SIZE_CHOICES = (
    ("Small | £50", "small | £50"),
    ("Normal | £80", "normal | £80"),
    ("Large | £100", "large | £100"),
    ("Extra-Large | £120", "extra-large | £120"),
)

PRICES = (
    ("50", "50"),
    ("80", "80"),
    ("100", "100"),
    ("120", "120"),
)

LENGTH_CHOICES = (
    ("Bra", "bra"),
    ("Mid-Back", "mid-back"),
    ("Waist", "waist"),
    ("Butt", "butt"),
    ("Mid Thighs", "mid thighs"),
    ("Knees", "knees"),
)


class Hairstyles(models.Model):
    title = models.CharField(max_length=200)
    duration = models.FloatField(null=True)
    image = models.ImageField(default='hairstyle4.jpg', upload_to='media/hairstyle_pictures', storage=MediaStorage)
    description = models.TextField(
        default='Please ensure your hair is washed thoroughly, blow dried and grease free!'
                ' - Expression Hair & Wax is provided by me!')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


# Generate hour choices from 9 AM to 9 PM with 1-hour increments

TIME_CHOICES = [(time(hour, 0), f'{hour:02d}:00') for hour in range(9, 18)]


class Appointment(models.Model):
    # data needed to be inputted from the user

    title = models.ForeignKey(Hairstyles, on_delete=models.CASCADE, related_name='hairstyles', default=Hairstyles)
    date = models.DateField(null=True, blank=False)
    time = models.TimeField(null=True, choices=TIME_CHOICES, blank=False)
    size_and_price = models.CharField(max_length=100, choices=SIZE_CHOICES, default=SIZE_CHOICES[1][0])
    price = models.PositiveIntegerField(choices=SIZE_CHOICES, null=True)
    length = models.CharField(max_length=100, choices=LENGTH_CHOICES, default=LENGTH_CHOICES[0][0])

    # Confirmation and keys to enable An appointment instances' flexibility on the site and with API's

    expired = models.BooleanField(default=False)
    client_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_confirmed = models.BooleanField(default=False)
    calendar_event_id = models.CharField(max_length=500, null=True)
    stripe_checkout_id = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.client_name}'s {self.title} Appointment on {self.date} @ {self.time}| eventID: {self.calendar_event_id}"


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    client_message = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}'s message"
