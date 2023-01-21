from __future__ import print_function

import datetime
from datetime import date
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dateutil import parser


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def _get_event():
    to_dos = []
    creds = None

    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        today_begin = datetime.datetime.combine(date.today(), datetime.time())
        today_beginning = today_begin.isoformat() + 'Z'
        today_end = today_begin + datetime.timedelta(days=1)
        today_ending = today_end.isoformat() + 'Z'

        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=today_beginning, timeMax=today_ending,
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            parsedDate = parser.parse(start)
            time = str(parsedDate.time())
            #print(time, event['summary'])
            to_dos.append("<u>" + time + "</u>" + " " + event['summary'].capitalize())

    except HttpError as error:
        print('An error occurred: %s' % error)

    return to_dos


if __name__ == '__main__':
    _get_event()
