import json

from django.db import models

from Ratatoskr.abstractNut import AbstractNut
from Ratatoskr.anotations import handler


class DataClass(AbstractNut):
    def handleCREATE(self, data):
        pass

    def handleUPDATE(self, data):
        pass

    def handleGET(self, data):
        pass

    name = models.CharField(max_length=255, default="abcd")
    email = models.EmailField()
    index = models.IntegerField()
    isActive = models.BooleanField()

    class Nuts:
        public = {'id', 'index', 'name', 'email', 'isActive'}
        index_by = 'id'

        assert(index_by in public)

