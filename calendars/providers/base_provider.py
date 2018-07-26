from abc import ABCMeta, abstractmethod


class AbstractProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config, credentialsDir):
        pass

    @abstractmethod
    def retrieveEventsByDate(self, startDate, endDate):
        pass
