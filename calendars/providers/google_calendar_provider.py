from base_provider import AbstractProvider
from calendar_event import CalendarEvent

from oauth2client import client, file
from apiclient.discovery import build
from httplib2 import Http
import dateutil.parser
import logging
import os.path

# https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/calendar&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob&client_id=173155842276-rfbrtra35u55rug7jtc85i50r9grunbg.apps.googleusercontent.com

USER_CRED_PATH = 'user_creds.json'
APP_CRED_PATH = 'app_creds.json'


def googleEventToCalendarEvent(googleEvent):
    event = CalendarEvent(
        title=googleEvent['summary'],
        startDate=apiFormatToDate(googleEvent['start']['dateTime']),
        endDate=apiFormatToDate(googleEvent['end']['dateTime']),
        description='')

    if 'description' in googleEvent:
        event.description = googleEvent['description']
    return event


def dateToApiFormat(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S')+'Z'


def apiFormatToDate(dateString):
    return dateutil.parser.parse(dateString)


class GoogleCalendarProvider(AbstractProvider):
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing Google Calendar provider')

        self.creds = None
        if os.path.isfile(USER_CRED_PATH):
            self.creds = file.Storage(USER_CRED_PATH).locked_get()
        else:
            self.logger.info('Attempting to retrieve new user credentials')
            if 'google_token' not in config:
                raise Exception('Unable to find Google  \
                                authorization code in action config')

            self.creds = client.credentials_from_clientsecrets_and_code(
                filename=APP_CRED_PATH,
                code=config['google_token'],
                scope='https://www.googleapis.com/auth/calendar',
                redirect_uri='urn:ietf:wg:oauth:2.0:oob')

            file.Storage(USER_CRED_PATH).locked_put(self.creds)
            self.logger.info('New credentials retrieved and stored')

        self.service = build('calendar', 'v3',
                             http=self.creds.authorize(Http()))

    def retrieveEventsByDate(self, startDate, endDate):
        response = self.service.events().list(
            calendarId='primary',
            singleEvents=True,
            orderBy='startTime',
            timeMin=dateToApiFormat(startDate),
            timeMax=dateToApiFormat(endDate)).execute()

        return [googleEventToCalendarEvent(evt)
                for evt in response.get('items', [])]
