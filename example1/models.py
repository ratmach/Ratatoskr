from django.db import models


class DataClass(models.Model):
    name = models.CharField(max_length=255, default="abcd")
    email = models.EmailField()
    index = models.IntegerField()
    isActive = models.BooleanField()

    class Nuts:
        public = ("name", "email", "isActive")