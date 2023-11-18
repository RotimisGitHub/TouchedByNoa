from django.shortcuts import render, redirect
import os
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME, EMAIL_HOST_PASSWORD
from .models import Hairstyles, Appointment
from .forms import AppointmentForm, ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .email_utils import send_appointment_confirmation_email


# Create your views here.

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


    if request.method == "POST":

        title = request.POST.get('title')
        size_and_price = request.POST.get('size_and_price')
        time = request.POST.get('time')
        date = request.POST.get('date')
        length = request.POST.get('length')
        form_data = {
            'title': title,
            'size_and_price': size_and_price,
            'time': time,
            'date': date,
            'length': length,
        }
        form = AppointmentForm(data=form_data)

        if form.is_valid() and request.POST.get("book"):
            form.instance.is_confirmed = True
            form.instance.client_name = request.user
            form.save()
            print("Before sending confirmation email")
            send_appointment_confirmation_email(form, email=request.user.email)
            print("After sending confirmation email")
            messages.success(request=request,
                             message=f"Your appointment has been booked! Please check your dashboard and email at "
                                     f"{request.user.email} for further confirmation!")
            return redirect("my-appointments")
    else:

        form = AppointmentForm()
        print(form.errors)

    context = {
        "form": form,

    }
    return render(request, "touchedbynoa/appointment.html", context)


@login_required
def my_appointment(request):
    appointments = Appointment.objects.filter(is_confirmed=True, client_name=request.user)

    context = {
        "appointments": appointments
    }
    return render(request, "touchedbynoa/my_appointment.html", context)


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

        if form.is_valid() and request.POST.get("book"):
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
