from django.contrib import admin
from .models import Hairstyles, Appointment, ContactUs

# Register your models here.

admin.site.register(Hairstyles)
admin.site.register(Appointment)
admin.site.register(ContactUs)
