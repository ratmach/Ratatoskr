import json

from django.db import models

from Ratatoskr.abstractNut import AbstractNut
from Ratatoskr.anotations import handler


class DataClass(models.Model):
    @handler(method="CREATE")
    def handleCREATE(self, data):
        tmp = DataClass.objects.create(name=data["name"],
                                       email=data["email"],
                                       index=0,
                                       isActive=data["isActive"] == "true")
        tmp.save()
        return tmp.JSON()

    @handler(method="nameLIKE")
    def handleLIKE(self, data):
        tmp = DataClass.objects.filter(name__contains=data["name"])
        return list(map(lambda x: x.id, tmp))

    @handler(method="UPDATE")
    def handleUPDATE(self, data):
        tmp = DataClass.objects.filter(id=data["id"])
        tmp = tmp.get()
        tmp.name = data["name"]
        tmp.name = data["email"]
        tmp.name = data["isActive"] == "true"
        tmp.save()
        return tmp.JSON()

    @handler(method="GET")
    def handleGET(self, data):
        tmp = DataClass.objects.filter(id=data["id"])
        return tmp.get().JSON()

    @handler(method="DELETE")
    def handleDELETE(self, data):
        print("Delete called")

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="abcd")
    email = models.EmailField()
    index = models.IntegerField()
    isActive = models.BooleanField()

    def JSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "index": self.index,
            "isActive": self.isActive
        }

    class Nuts:
        public = {'id', 'index', 'name', 'email', 'isActive'}
        index_by = 'id'

        assert (index_by in public)

    class Meta:
        verbose_name = "DataClass"
