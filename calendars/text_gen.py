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

    return date >= todayStart and date < todayEnd


def isTomorrow(date):
    tomorrow = datetime.datetime.today() \
        + datetime.timedelta(days=1)
    tomorrowStart = utc.localize(datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day))
    tomorrowEnd = utc.localize(datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59))

    return date >= tomorrowStart and date < tomorrowEnd


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


def timeAsSpoken(time):
    hour = time.hour
    minute = time.minute

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


def dateAsSpoken(date):
    date = utc.localize(datetime.datetime(date.year, date.month, date.day))

    if isToday(date):
        return 'today'
    elif isTomorrow(date):
        return 'tomorrow'
    else:
        return 'on the ' + numberToOrdinal(date.day) \
            + ' of ' + monthAsSpoken(date.month)


def eventsAsSpoken(events):
    buf = ''

    for date in events:
        dayEvents = events[date]
        buf += dateAsSpoken(date)
        for event in dayEvents:
            buf += ' at ' + timeAsSpoken(event.startDate.time()) \
                + '. ' + event.title + '. '
    return buf
