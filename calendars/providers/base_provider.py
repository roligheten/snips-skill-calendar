from abc import ABCMeta, abstractmethod


class AbstractProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def retrieveEventsByDate(self, startDate, endDate):
        pass
