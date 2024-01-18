import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build


def create_calendar_event(appointment_title,
                          appointment_datetime,
                          appointment_end_time,
                          client_user_email,
                          event_id,
                          payment_type

                          ):
    CLIENT_SECRET_FILE = "sensitive/credentials.json"
    calendar_id = os.environ.get("CALENDER_ID")
    API_KEY = os.environ.get("CALENDER_API_KEY")
    email = os.environ.get("BUSINESS_EMAIL")

    credentials = service_account.Credentials.from_service_account_file(
        CLIENT_SECRET_FILE,
        scopes=['https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                'https://www.googleapis.com/auth/calendar.events'],
        subject=email
    )

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'id': event_id,
        'summary': 'Hair Appointments',
        'location': os.environ.get("TOUCHEDBYNOA_ADDRESS"),
        'description': f'{payment_type}: {appointment_title} for {client_user_email}',
        'start': {
            'dateTime': appointment_datetime,
            'timeZone': 'GMT+00:00',
        },
        'end': {
            'dateTime': appointment_end_time,
            'timeZone': 'GMT+00:00',
        },
        'attendees': [
            {'email': f'{client_user_email}'},
            {'email': 'touchedbynoa@gmail.com'}
        ],

        'transparency': 'opaque',
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 3 * 60},
            ],
        },
    }

    service.events().insert(calendarId=calendar_id, body=event, sendUpdates='all', key=API_KEY).execute()


def delete_calender_event(eventID):
    CLIENT_SECRET_FILE = "sensitive/credentials.json"
    calendar_id = os.environ.get("CALENDER_ID")
    API_KEY = os.environ.get("CALENDER_API_KEY")
    email = os.environ.get("BUSINESS_EMAIL")

    credentials = service_account.Credentials.from_service_account_file(
        CLIENT_SECRET_FILE,
        scopes=['https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                'https://www.googleapis.com/auth/calendar.events'],
        subject=email
    )

    service = build('calendar', 'v3', credentials=credentials)

    event_id_to_delete = f'{eventID}'

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


def check_booked_times(chosen_date):
    CLIENT_SECRET_FILE = "sensitive/credentials.json"
    calendar_id = os.environ.get("CALENDER_ID")
    email = os.environ.get("BUSINESS_EMAIL")

    time_min = chosen_date.isoformat() + 'Z'
    time_max = (chosen_date + relativedelta(weeks=4)).isoformat() + 'Z'
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    credentials = service_account.Credentials.from_service_account_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, subject=email)

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
            date, start_time, end_time = start.split("T")[0], start.split("T")[1].replace("Z", ""), end.split("T")[
                1].replace("Z", "")

            # Create a new dictionary for each event
            event_dict = {
                "date": date,
                "start_time": datetime.strptime(start_time, "%H:%M:%S").hour,
                "end_time": datetime.strptime(end_time, "%H:%M:%S").hour
            }

            # Append the dictionary to the list
            booked_times.append(event_dict)

    return booked_times
