# DJANGO LIBRARIES
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.urls import reverse_lazy

# APPLICATION LIBRARIES
from config import settings
from .models import *
from .forms import *
from .utils import *
# OTHERS

import time, stripe, secrets

stripe.api_key = settings.STRIPE_SECRET_KEY
def home_page(request):
    return render(request, "touchedbynoa/home.html")


def hairstyles(requests):
    hairstyles = Hairstyles.objects.filter(is_active=True)

    context = {
        "hairstyles": hairstyles
    }
    return render(requests, 'touchedbynoa/hairstyles.html', context)


@login_required()
def appointment(request):

    if request.POST.get('date'):
        print(check_booked_times())

    if request.method == 'POST':
        title = request.POST.get('title')
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
            cancel_url=settings.REDIRECT_DOMAIN + '/appointments',
        )
        checkout_session_id = checkout_session['id']

        form_data = {
            'title': title,
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
            form.save()

            return redirect(checkout_session.url, code=303)

    else:

        form = AppointmentForm()
        print(form.errors)

    context = {
        "form": form,

    }
    return render(request, "touchedbynoa/appointment.html", context)


@login_required
def payment_success(request):
    checkout_session_id = request.GET.get('session_id', None)
    appointment_instance = Appointment.objects.get(stripe_checkout_id=checkout_session_id)

    start_and_end = convert_time_then_add(date=appointment_instance.date, time=appointment_instance.time,
                                          duration=appointment_instance.title.duration)
    start_time = start_and_end[0]
    end_time = start_and_end[1]

    create_calendar_event(
        appointment_title=appointment_instance.title,
        appointment_datetime=start_time,
        appointment_time_duration=end_time,
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


def contact(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            name = request.user.username
            email = request.user.email
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')

        client_messages = request.POST.get('client_message')

        form_data = {
            'name': name,
            'email': email,
            'client_message': client_messages,

        }
        form = ContactForm(data=form_data)

        if form.is_valid():
            form.instance.is_confirmed = True
            form.instance.client_name = request.user
            form.save()
            messages.success(request=request,
                             message=f"Thank you! Your message has been sent and we are trying our best to get back to "
                                     f"you when we can!")
            return redirect("contact-us")
    else:

        form = ContactForm()
        print(form.errors)

    context = {
        "form": form,

    }
    return render(request, "touchedbynoa/contact_us.html", context)
