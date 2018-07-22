import text_gen
from datetime import datetime, timedelta


def endOfHour(date):
    return datetime(date.year, date.month, date.day, date.hour, 59, 59)


def endOfDay(date):
    return datetime(date.year, date.month, date.day, 23, 59, 59)


def endOfWeek(date):
    date = endOfDay(date)
    return date - timedelta(days=date.weekday()) + timedelta(days=6)


def summerizeEvents(provider, date, grain):
    events = None

    assumeDateKnown = False
    if grain == 'Hour':
        assumeDateKnown = True
        events = provider.retrieveEventsByDate(date, endOfHour(date))
    elif grain == 'Day':
        # Summerize all events of the day
        assumeDateKnown = True
        events = provider.retrieveEventsByDate(date, endOfDay(date))
    elif grain == 'Week':
        assumeDateKnown = False
        events = provider.retrieveEventsByDate(date, endOfWeek(date))
    else:
        # TODO: Handle remaining granularities
        pass
    if events is None or len(events) == 0:
        return 'You have no events scheduled at the given time'

    return text_gen.eventsAsSpoken(events, assumeDateKnown)
