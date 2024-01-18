
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="home"),
    path('hairstyles/', hairstyles, name="hairstyles"),
    path('prices/', price_guide, name="prices"),
    path('appointments/<int:pk>/', AppointmentView.as_view(), name="appointments"),
    path('api/available_times/', AvailableTimesAPIView, name="api-appointments"),
    path('my-appointments/', my_appointment, name="my-appointments"),
    path('payment_successful/', payment_success, name="payment-success"),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('my-appointments/<int:pk>/detail', AppointmentDetail.as_view(), name="appointment-detail"),
    path('my-appointments/<int:pk>/cancel', CancelAppointment.as_view(), name="cancel-my-appointments")

]

