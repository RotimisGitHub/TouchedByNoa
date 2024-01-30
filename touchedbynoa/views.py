# DJANGO LIBRARIES
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.urls import reverse_lazy

from rest_framework import status

# APPLICATION LIBRARIES
from config import settings
from .models import *
from .forms import *
from .utils import *
# OTHERS

import time, stripe, secrets
from datetime import time

stripe.api_key = settings.STRIPE_SECRET_KEY


def home_page(request):
    return render(request, "touchedbynoa/home.html")


def hairstyles(request):
    ponytails = Hairstyles.objects.filter(is_active=True, style="Ponytails")
    cornrows = Hairstyles.objects.filter(is_active=True, style="Cornrows")
    knotless = Hairstyles.objects.filter(is_active=True, style="Knotless")

    context = {
        "ponytails": ponytails,
        "cornrows": cornrows,
        "knotless": knotless,
    }

    response = render(request, 'touchedbynoa/hairstyles.html', context)

    return response

def price_guide(request):
    ponytails = Hairstyles.objects.filter(title="2 Pig Ponytails")
    cornrows = Hairstyles.objects.filter(title="Snake Heart Feed")
    knotless = Hairstyles.objects.filter(title="Fulani Braids")

    context = {
        "ponytails": ponytails,
        "cornrows": cornrows,
        "knotless": knotless,
    }

    return render(request, 'touchedbynoa/price_guide.html', context)

def AvailableTimesAPIView(request):
    try:
        selected_date = json.loads(request.body)
        date = selected_date.get("selected_date")
    except json.JSONDecodeError:

        return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    if date is None:
        return JsonResponse({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)

    booked_appointments = check_booked_times(datetime.strptime(date, "%Y-%m-%d"))
    available_times = []

    # Iterate over the booked appointments
    for appointment in booked_appointments:
        # Check if the appointment date matches the selected date
        if appointment["date"] == date:
            # Extract the start and end times
            start_time = appointment["start_time"]
            end_time = appointment["end_time"]

            available_times.append(start_time)
            available_times.append(end_time)

    if len(available_times) > 0:

        available_times = [
            f'{hour:02d}:00' for hour in range(9, 21) if hour < available_times[0] or available_times[1] >= hour
        ]
    else:
        available_times = [f'{hour:02d}:00' for hour in range(9, 21)]

    # Return a valid JSON response
    return JsonResponse({'available_times': available_times}, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class AppointmentView(View):
    template_name = "touchedbynoa/appointment.html"

    def get(self, request, pk):
        form = AppointmentForm()
        print(form.errors)

        hairstyle = Hairstyles.objects.get(id=pk)

        context = {
            "form": form,
            "hairstyle": hairstyle
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        hairstyle = Hairstyles.objects.get(id=pk)

        size_and_price = request.POST.get('size_and_price')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        length = request.POST.get('length')
        calendar_event_id = secrets.token_hex(12)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + f'/appointments/{pk}/',  # Adjust cancel URL
        )
        checkout_session_id = checkout_session['id']

        form_data = {
            'title': hairstyle.title,
            'size_and_price': size_and_price,
            'date': date_str,
            'time': time_str,
            'length': length,
            'eventID': calendar_event_id,
        }
        form = AppointmentForm(data=form_data)

        if form.is_valid() and request.POST.get('book'):
            form.instance.stripe_checkout_id = checkout_session_id
            form.instance.client_name = request.user
            form.instance.calendar_event_id = calendar_event_id
            form.instance.title = hairstyle # since its a foreign key field, it will inherit the title of the chose hairstyle
            form.save()

            return redirect(checkout_session.url, code=303)

        context = {
            "form": form,
            "hairstyle": Hairstyles.objects.get(id=pk),
        }

        return render(request, self.template_name, context)


@login_required
def payment_success(request):

    checkout_session_id = request.GET.get('session_id', None)
    appointment_instance = Appointment.objects.get(stripe_checkout_id=checkout_session_id)

    appointment_times = convert_time_then_add(date=appointment_instance.date, time=appointment_instance.time,
                                          duration=appointment_instance.title.duration)

    start_time, end_time = appointment_times[0], appointment_times[1]

    create_calendar_event(
        appointment_title=appointment_instance.title,
        appointment_datetime=start_time,
        appointment_end_time=end_time,
        client_user_email=request.user.email,
        event_id=appointment_instance.calendar_event_id,
        payment_type="DEPOSIT")

    appointment_instance.is_confirmed = True
    appointment_instance.save()

    messages.success(request=request,
                     message=f"Your appointment has been booked! Please check your dashboard and email at "
                             f"{request.user.email} for further confirmation!")

    return render(request, 'touchedbynoa/payment_successful.html', context={"appointment": appointment_instance})


@login_required
def my_appointment(request):
    appointments = Appointment.objects.filter(is_confirmed=True, client_name=request.user)

    context = {
        "appointments": appointments
    }
    return render(request, "touchedbynoa/my_appointment.html", context)


def payment_cancelled(request):
    checkout_session_id = request.GET.get('session_id', None)
    appointment_payment = Appointment.objects.get(stripe_checkout_id=checkout_session_id)
    appointment_payment.delete()
    messages.error(request=request,
                   message="Your payment was either cancelled or unsuccessful!")
    return render(request, 'touchedbynoa/appointment.html')


@csrf_exempt
def stripe_webhook(request):
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
    return HttpResponse(status=200)


class AppointmentDetail(DetailView):
    model = Appointment
    template_name = 'touchedbynoa/appointment_detail.html'


class CancelAppointment(DeleteView):
    model = Appointment
    success_url = reverse_lazy('my-appointments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_view'] = True
        apps = \
            str(Appointment.objects.filter(id=self.kwargs.get('pk'))).split("<QuerySet [<Appointment:")[1].split(">]>")[
                0]
        context['edit_appointment_name'] = apps
        return context

    def form_valid(self, form):
        # object to be deleted
        obj = self.get_object()

        # custom logic for sending email on successful deletion
        try:
            delete_calender_event(eventID=obj.calendar_event_id)
            # Perform the deletion
            response = super().form_valid(form)

            messages.success(self.request, 'Successfully Cancelled Your Appointment.')

            return response
        except Exception as e:
            # If deletion fails
            messages.error(self.request, 'Deletion failed. Please try again.')
            # Redirect to a different URL on failure
            return self.get_failure_url()

    def get_failure_url(self):
        #  URL to redirect to on deletion failure
        return reverse_lazy('my-appointments')
