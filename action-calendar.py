import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime, timedelta
import dateutil.parser
import logging
import logging.config
from sys import exit

from snipshelpers.config_parser import SnipsConfigParser
import snipshelpers.intent_helper
from calendars.providers import GoogleCalendarProvider
from calendars import summerizeEvents

MQTT_IP_ADDR = "raspberrypi.local"
MQTT_PORT = 1883

CONFIGURATION_ENCODING_FORMAT = "utf-8"
SNIPS_CONF = 'config.ini'
LOGGER_CONF = 'logger_conf.json'

INT_QUERYNEXT = 'hermes/intent/chrbarrol:queryNextEvent'
INT_EVENTSAT = 'hermes/intent/chrbarrol:queryEventsAtDate'

mqttCli = None
skill = None


def endOfHour(date):
    return datetime(date.year, date.month, date.day, date.hour, 59, 59)


def endOfDay(date):
    return datetime(date.year, date.month, date.day, 23, 59, 59)


def endOfWeek(date):
    date = endOfDay(date)
    return date - timedelta(days=date.weekday()) + timedelta(days=6)


def resolveGrainToDate(date, grain):
    if grain == 'Hour':
        return endOfHour(date)
    if grain == 'Day':
        return endOfDay(date)
    elif grain == 'Week':
        return endOfWeek(date)
    else:
        return None


class Skill:
    def __init__(self, cli):
        self.logger = logging.getLogger(__name__)
        self.config = SnipsConfigParser.read_configuration_file(SNIPS_CONF)
        self.mqttClient = cli

        self.provider = GoogleCalendarProvider(self.config['secret'])

    def handleIntent(self, sessionId, intent, slots):
        if intent == INT_EVENTSAT:
            self.logger.info('Handling topic \'%s\'', intent)
            self.respond_eventsAt(sessionId, slots)
        else:
            self.logger.warn('Asked to handle unknown topic \'%s\'', intent)
            pass

    def respond_eventsAt(self, sessionId, slots):
        startDate = datetime.today()
        endDate = None

        # TODO: Handle multiple dates given
        matchedSlot = snipshelpers.intent_helper \
            .getFirstBySlotName(slots, 'date')

        response = None
        if matchedSlot is not None:
            val = matchedSlot['value']
            if val['kind'] == 'InstantTime':
                startDate = dateutil.parser.parse(val['value'])
                endDate = resolveGrainToDate(startDate, val['grain'])
            elif val['kind'] == 'TimeInterval':
                startDate = dateutil.parser.parse(val['from'])
                endDate = dateutil.parser.parse(val['to'])
        else:
            # If not slot exists assume user asked for events today
            endDate = resolveGrainToDate(startDate, 'Day')

        response = None
        if endDate is None:
            response = "Sorry, I cannot answer that question."
        else:
            response = summerizeEvents(self.provider, startDate, endDate)

        self.mqttClient.publish('hermes/dialogueManager/endSession',
                                json.dumps({
                                    'sessionId': sessionId,
                                    'text': response
                                }))


def onMessage(client, userData, message):
    logger = logging.getLogger(__name__)
    payload = json.loads(message.payload)

    try:
        skill.handleIntent(payload['sessionId'],
                           message.topic,
                           payload['slots'])
    except Exception:
        logger.exception('Failed to answer query')


def onConnect(client, userData, flags, rc):
    logger = logging.getLogger(__name__)
    logger.info('Connected to MQTT broker')

    try:
        mqttCli.subscribe(INT_QUERYNEXT)
        mqttCli.subscribe(INT_EVENTSAT)
    except Exception:
        logger.exception('Failed subscribing to topic')


if __name__ == '__main__':
    logger = None
    try:
        with open(LOGGER_CONF, 'rt') as loggerConfFile:
            loggerConf = json.loads(loggerConfFile.read())
            logging.config.dictConfig(loggerConf)
            logger = logging.getLogger(__name__)
    except Exception:
        logging.exception('Failed to load configuration from file')
        exit(-1)

    logger.info('Connecting to MQTT broker')
    try:
        mqttCli = mqtt.Client()
        mqttCli.on_connect = onConnect
        mqttCli.on_message = onMessage
        mqttCli.connect(MQTT_IP_ADDR, MQTT_PORT)

        mqttCli.loop_start()
    except Exception:
        logger.exception('Failed to initialize MQTT connection')
        exit(-1)

    logger.info('Calendar action initializing')
    try:
        skill = Skill(mqttCli)
    except Exception:
        logger.exception('Failed to initialize skill')
        exit(-1)

    shouldStop = False
    try:
        while not shouldStop:
            time.sleep(0.1)
    except KeyboardInterrupt:
        mqttCli.loop_stop()
        mqttCli.disconnect()
        shouldStop = True
