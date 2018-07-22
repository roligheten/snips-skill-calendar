import datetime
import pytz

utc = pytz.UTC


def numberToOrdinal(number):
    return "%d%s" % (number, "tsnrhtdd"[(number/10%10!=1)*(number%10<4)*number%10::4])


def monthAsSpoken(month):
    if month == 1:
        return 'january'
    elif month == 2:
        return 'febuary'
    elif month == 3:
        return 'march'
    elif month == 4:
        return 'april'
    elif month == 5:
        return 'may'
    elif month == 6:
        return 'june'
    elif month == 7:
        return 'july'
    elif month == 8:
        return 'august'
    elif month == 9:
        return 'september'
    elif month == 10:
        return 'october'
    elif month == 11:
        return 'november'
    elif month == 12:
        return 'december'


def isToday(date):
    today = datetime.datetime.today()
    todayStart = utc.localize(datetime.datetime(today.year,
                                                today.month,
                                                today.day))
    todayEnd = utc.localize(datetime.datetime(today.year,
                                              today.month,
                                              today.day,
                                              23, 59, 59))

    print(date, todayStart)
    return date > todayStart and date <= todayEnd


def isTomorrow(date):
    tomorrow = datetime.datetime.today() \
        + datetime.timedelta(days=1)
    tomorrowStart = utc.localize(datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day))
    tomorrowEnd = utc.localize(datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59))

    return date > tomorrowStart and date <= tomorrowEnd


def timeOfDayAsSpoken(hour, minute):
    period = 'am'
    if hour >= 12:
        period = 'pm'
        if hour > 12:
            hour -= 12
    elif hour == 0:
        hour = 12

    buf = str(hour) + ':'
    if minute < 10:
        buf += '0'
    buf += str(minute) + ' '
    buf += period

    return buf


def dateAsSpoken(date, includeDate, includeTime):
    if not includeDate and not includeTime:
        raise RuntimeError('Cannot build date string without date or time')

    buf = ''
    if includeDate:
        buf += numberToOrdinal(date.day) + ' of ' + monthAsSpoken(date.month)
    if includeTime:
        if includeDate:
            buf += ' at '
        buf += timeOfDayAsSpoken(date.hour, date.minute)
    return buf


def eventAsSpoken(event, assumeDateKnown=False):
    buf = None
    if assumeDateKnown:
        buf = 'at ' + dateAsSpoken(event.startDate, False, True)
    elif isToday(event.startDate):
        buf = 'today at ' + dateAsSpoken(event.startDate, False, True)
    elif isTomorrow(event.startDate):
        buf = 'tomorrow at ' + dateAsSpoken(event.startDate, False, True)
    else:
        buf = 'on the ' + dateAsSpoken(event.startDate, True, True)

    buf += ' . ' + event.title
    return buf


def eventsAsSpoken(events, assumeDateKnown):
    buf = None

    for event in events:
        if buf is None:
            buf = eventAsSpoken(event, assumeDateKnown)
        else:
            buf += '. ' + eventAsSpoken(event, assumeDateKnown)
    return buf
