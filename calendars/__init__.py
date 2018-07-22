import text_gen
from datetime import datetime, timedelta
from collections import OrderedDict

def groupEventsByDay(events):
    eventMap = OrderedDict()
    for event in events:
        eventDate = event.startDate.date()
        if eventDate in eventMap:
            eventMap[eventDate].append(event)
        else:
            eventMap[eventDate] = [event]
    return eventMap


def summerizeEvents(provider, startDate, endDate):
    events = groupEventsByDay(provider.retrieveEventsByDate(startDate,
                                                            endDate))

    if events is None or len(events) == 0:
        return 'You have no events scheduled at the given time'

    return text_gen.eventsAsSpoken(events)
