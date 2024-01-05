import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build


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
        'visibility': 'frontend_images',
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

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

def check_booked_times(service_account_file='sensitive/credentials.json', calendar_id=os.environ.get("CALENDER_ID"), time_min='2023-12-21T00:00:00Z', time_max='2023-12-31T00:00:00Z'):
    # Set up the service account credentials
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)

    # Build the service using the credentials
    service = build('calendar', 'v3', credentials=credentials)

    # Call the Google Calendar API to retrieve events
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    # Get the events from the response
    events = events_result.get('items', [])

    # Process the events
    booked_times = []
    if events:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            date, start_time, end_time = start.split("T")[0], start.split("T")[1].replace("Z", ""), end.split("T")[1].replace("Z", "")
            booked_times.append((date, start_time, end_time, event.get('summary', '')))

    return booked_times
