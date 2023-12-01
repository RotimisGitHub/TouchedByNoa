
from django.urls import path
from .views import hairstyles, home_page, appointment, my_appointment, contact, CancelAppointment, AppointmentDetail, \
    stripe_webhook, payment_success

urlpatterns = [
    path('', home_page, name="home"),
    path('hairstyles/', hairstyles, name="hairstyles"),
    path('appointments/', appointment, name="appointments"),
    path('my-appointments/', my_appointment, name="my-appointments"),
    path('payment_successful/', payment_success, name="payment-success"),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('my-appointments/<int:pk>/detail', AppointmentDetail.as_view(), name="appointment-detail"),
    path('my-appointments/<int:pk>/cancel', CancelAppointment.as_view(), name="cancel-my-appointments"),



    path('contact/', contact, name="contact-us"),

]

