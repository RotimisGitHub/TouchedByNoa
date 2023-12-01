import os
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

'''
# Old Confirmation Method 
# (Still can be used for reference in the future :) )

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import config.settings

def send_appointment_confirmation_email(appointment, email):
    subject = 'Appointment Confirmation'
    from_email = config.settings.EMAIL_HOST_USER
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


def send_appointment_deleted_email(appointment, email):
    subject = 'Appointment Cancelled'
    from_email = config.settings.EMAIL_HOST_USER
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

'''


def create_calendar_event(appointment_title,
                          appointment_datetime,
                          appointment_time_duration,
                          client_user_email,
                          event_id,
                          payment_type
                          ):
    # service account details
    CLIENT_SECRET_FILE = "sensitive/credentials.json"

    credentials = service_account.Credentials.from_service_account_file(
        CLIENT_SECRET_FILE,
        scopes=['https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                'https://www.googleapis.com/auth/calendar.events'],
        subject=os.environ.get("BUSINESS_EMAIL")
    )

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'id': event_id,
        'summary': 'Hair Appointments',
        'location': os.environ.get("TOUCHEDBYNOA_ADDRESS"),
        'description': f'{payment_type}: {appointment_title}',
        'start': {
            'dateTime': appointment_datetime,
            'timeZone': 'GMT+00:00',
        },
        'end': {
            'dateTime': appointment_time_duration,
            'timeZone': 'GMT+00:00',
        },
        'attendees': [
            {'email': f'{client_user_email}'},
            {'email': 'touchedbynoa@gmail.com'},
        ],

        'transparency': 'opaque',
        'visibility': 'public',
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 3 * 60},
            ],
        },
    }

    calendar_id = os.environ.get("CALENDER_ID")
    API_KEY = os.environ.get("CALENDER_API_KEY")

    service.events().insert(calendarId=calendar_id, body=event, sendUpdates='all', key=API_KEY).execute()


def delete_calender_event(eventID):
    credentials = service_account.Credentials.from_service_account_file(
        'sensitive/credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                'https://www.googleapis.com/auth/calendar.events'],
        subject=os.environ.get("BUSINESS_EMAIL")
    )

    service = build('calendar', 'v3', credentials=credentials)

    event_id_to_delete = f'{eventID}'

    calendar_id = os.environ.get("CALENDER_ID")
    API_KEY = os.environ.get("CALENDER_API_KEY")

    # Call the Calendar API to delete the event
    service.events().delete(calendarId=calendar_id, eventId=event_id_to_delete, sendUpdates='all',
                            key=API_KEY).execute()



def convert_time_then_add(date, time, duration):
    datetime_str = f"{date}T{time}:00"
    duration_hours = duration
    start_time = datetime.fromisoformat(datetime_str)
    added_time = start_time + timedelta(hours=duration_hours)
    end_time = added_time.isoformat()
    return start_time.isoformat(), end_time

