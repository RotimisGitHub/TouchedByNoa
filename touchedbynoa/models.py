from django.db import models
from users.models import CustomUser
from config.storage_backends import MediaStorage
from django.contrib.auth import get_user_model

User = get_user_model()

SIZE_CHOICES = (
    ("Small", "Small"),
    ("S/Medium", "S/Medium"),
    ("Medium", "Medium"),
    ("Large", "Large"),
    ("Extra Large", "Extra Large"),
)

LENGTH_CHOICES = (
    ("Bra", "Bra"),
    ("Mid-Back", "Mid-Back"),
    ("Waist", "Waist"),
    ("Mid Thighs", "Mid Thighs"),
    ("Knees", "Knees"),
)

STYLE_CHOICES = (
        ('Knotless', 'Knotless'),
        ('Cornrows', 'Cornrows'),
        ('Ponytails', 'Ponytails'),
)

class Hairstyles(models.Model):
    title = models.CharField(max_length=200)
    style = models.CharField(max_length=100, choices=STYLE_CHOICES, default=STYLE_CHOICES[0][0])
    duration = models.FloatField(null=True)
    image = models.ImageField(default='hairstyle4.jpg', upload_to='media/hairstyle_pictures', storage=MediaStorage)
    description = models.TextField(
        default='Please ensure your hair is washed thoroughly, blow dried and grease free!'
                ' - Expression Hair & Wax is provided by me!')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Appointment(models.Model):
    # data needed to be inputted from the user

    title = models.ForeignKey(Hairstyles, on_delete=models.CASCADE, related_name='hairstyles', null=True)
    date = models.DateField(null=True, blank=False)
    time = models.TimeField(null=True, blank=False)
    size_and_price = models.CharField(max_length=100, choices=SIZE_CHOICES, default=SIZE_CHOICES[3][0])
    length = models.CharField(max_length=100, choices=LENGTH_CHOICES, default=LENGTH_CHOICES[0][0])

    # Confirmation and keys to enable An appointment instances' flexibility on the site and with API's

    expired = models.BooleanField(default=False)
    client_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_confirmed = models.BooleanField(default=False)
    calendar_event_id = models.CharField(max_length=500, null=True)
    stripe_checkout_id = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.client_name}'s {self.title} Appointment on {self.date} @ {self.time}| eventID: {self.calendar_event_id}"
