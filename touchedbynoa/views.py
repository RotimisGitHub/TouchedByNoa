from django.shortcuts import render, redirect
from config import settings
from .models import Hairstyles, Appointment
from .forms import AppointmentForm, ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import create_calendar_event, delete_calender_event
from django.views.generic import DetailView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime, timedelta
import stripe
import secrets


def home_page(request):
    return render(request, "touchedbynoa/home.html")


def hairstyles(requests):
    hairstyles = Hairstyles.objects.filter(is_active=True)

    context = {
        "hairstyles": hairstyles
    }
    return render(requests, 'touchedbynoa/hairstyles.html', context)


@login_required
def appointment(request):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': 'price_1OI1IFAH7CmnuovAjOi6JBEy',
                'quantity': 1,
            },
        ],
        mode='payment',
        customer_email=request.user.email,
        success_url='http://127.0.0.1:8000/'+ settings.LOGIN_REDIRECT_URL + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/'+ settings.LOGIN_REDIRECT_URL + '/payment_cancelled',
    )
    if request.method == "POST":

        title = request.POST.get('title')
        size_and_price = request.POST.get('size_and_price')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        length = request.POST.get('length')
        event_id = secrets.token_hex(12)

        form_data = {
            'title': title,
            'size_and_price': size_and_price,
            'date': date_str,
            'time': time_str,
            'length': length,
            'eventID': event_id,
        }

        form = AppointmentForm(data=form_data)

        if form.is_valid() and checkout_session:
            form.instance.is_confirmed = True
            form.instance.client_name = request.user
            form.instance.eventID = event_id
            form.save()

            # send_appointment_confirmation_email(form, email=request.user.email)
            datetime_str = f"{date_str}T{time_str}:00"
            duration_hours = form.instance.title.duration
            start_time = datetime.fromisoformat(datetime_str)
            added_time = start_time + timedelta(hours=duration_hours)
            end_time = added_time.isoformat()

            payment_status = "DEPOSIT"

            create_calendar_event(

                appointment_title=title,
                appointment_datetime=start_time.isoformat(),
                appointment_time_duration=end_time,
                client_user_email=request.user.email,
                event_id=form.instance.eventID,
                payment_type=payment_status)

            messages.success(request=request,
                             message=f"Your appointment has been booked! Please check your dashboard and email at "
                                     f"{request.user.email} for further confirmation!")
            return redirect("my-appointments")

    else:

        form = AppointmentForm()
        print(form.errors)

        context = {
            "form": form,
            'checkout_session_id': checkout_session.id

        }
        return render(request, "touchedbynoa/appointment.html", context)


@login_required
def my_appointment(request):
    appointments = Appointment.objects.filter(is_confirmed=True, client_name=request.user)

    context = {
        "appointments": appointments
    }
    return render(request, "touchedbynoa/my_appointment.html", context)


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
            delete_calender_event(eventID=obj.eventID)
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
