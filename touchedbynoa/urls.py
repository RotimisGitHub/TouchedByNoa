
from django.urls import path
from .views import hairstyles, home_page, appointment, my_appointment, contact


urlpatterns = [
    path('', home_page, name="home"),
    path('hairstyle/', hairstyles, name="hairstyles"),
    path('appointments/', appointment, name="appointments"),
    path('my-appointments/', my_appointment, name="my-appointments"),
    path('contact/', contact, name="contact-us"),

]
