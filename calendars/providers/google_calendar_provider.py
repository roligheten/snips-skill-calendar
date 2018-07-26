from base_provider import AbstractProvider
from calendar_event import CalendarEvent

from oauth2client import client, file
from apiclient.discovery import build
from httplib2 import Http
import dateutil.parser
import logging
import os.path

# https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/calendar&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob&client_id=173155842276-rfbrtra35u55rug7jtc85i50r9grunbg.apps.googleusercontent.com

USER_CRED_NAME = 'google_calendar_creds.json'
APP_CRED_PATH = 'app_creds.json'
APP_LOGGER = 'CalendarApp'


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


def saveCredentials(credentialsPath, credentials):
    file.Storage(credentialsPath).locked_put(credentials)


def retrieveNewCredentials(authenticationCode):
    return client.credentials_from_clientsecrets_and_code(
        filename=APP_CRED_PATH,
        code=authenticationCode,
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')


def retrieveStoredCredentials(credentialsPath):
    if os.path.isfile(credentialsPath):
        return file.Storage(credentialsPath).locked_get()
    else:
        return None


def buildGoogleApiService(credentials):
    return build('calendar', 'v3', http=credentials.authorize(Http()))


class GoogleCalendarProvider(AbstractProvider):
    def __init__(self, config, credentialsDir):
        self.logger = logging.getLogger(APP_LOGGER)
        self.logger.info('Initializing Google Calendar provider')

        credentialsPath = '{}/{}'.format(credentialsDir, USER_CRED_NAME)
        self.creds = retrieveStoredCredentials(credentialsPath)

        if self.creds is None:
            self.logger.info('No stored credentials found, retrieving new')
            if 'google_token' not in config or config['google_token'] == '':
                raise Exception('Unable to find Google '
                                + 'authorization code in action config')
            self.creds = retrieveNewCredentials(config['google_token'])
            saveCredentials(credentialsPath, self.creds)
            self.logger.info('New credentials retrieved and stored')
        else:
            self.logger.info('Existing credentials retrieved from disk')
        self.service = buildGoogleApiService(self.creds)

    def retrieveEventsByDate(self, startDate, endDate):
        response = self.service.events().list(
            calendarId='primary',
            singleEvents=True,
            orderBy='startTime',
            timeMin=dateToApiFormat(startDate),
            timeMax=dateToApiFormat(endDate)).execute()

        return [googleEventToCalendarEvent(evt)
                for evt in response.get('items', [])]
