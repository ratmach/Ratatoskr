import json

from django.db import models
from Ratatoskr.anotations import handler


class DataClass(models.Model):
    name = models.CharField(max_length=255, default="abcd")
    email = models.EmailField()
    index = models.IntegerField()
    isActive = models.BooleanField()

    class Nuts:
        public = {'id', 'index', 'name', 'email', 'isActive'}
        #TODO ordering

        index_by = 'id'

        assert(index_by in public)

    @handler(method="GET")
    def handle(self, data):
        print("data received: ", data)
        #THIS IS TEMPORARILY MOCK
        return json.dumps({"name": "rati", "email": "rmach13@freeuni.edu.ge", "index": 1, "isActive": True})
