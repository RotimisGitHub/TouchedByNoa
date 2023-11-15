from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def send_appointment_confirmation_email(appointment, email):
    subject = 'Appointment Confirmation'
    from_email = 'homebodyplug@gmail.com'
    recipient_list = [email]  # Replace with the actual recipient's email

    # Load and render the HTML email template with appointment data
    context = {
        'client_name': email,
        'appointment': appointment
    }
    html_message = render_to_string('touchedbynoa/appointment_confirmation.html', context)

    # Create a plain text version of the email (optional)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)
