from django.db import models
from Ratatoskr.anotations import handler


class DataClass(models.Model):
    name = models.CharField(max_length=255, default="abcd")
    email = models.EmailField()
    index = models.IntegerField()
    isActive = models.BooleanField()

    @handler(method="GET")
    def handle(self,data):
        print("data received: ",data)

