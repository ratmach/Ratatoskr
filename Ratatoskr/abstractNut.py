from abc import ABCMeta, abstractmethod
from django.db import models

from Ratatoskr.anotations import handler


class AbstractNut(models.Model):
    __metaclass__ = ABCMeta

    class Nuts:
        ignore_flag = True
        __metaclass__ = ABCMeta

    @handler(method="GET")
    @abstractmethod
    def handleGET(self, data):
        return NotImplemented

    @handler(method="CREATE")
    @abstractmethod
    def handleCREATE(self, data):
        return NotImplemented

    @handler(method="UPDATE")
    @abstractmethod
    def handleUPDATE(self, data):
        return NotImplemented

    @abstractmethod
    def JSON(self):
        return NotImplemented