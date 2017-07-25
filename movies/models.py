from django.db import models

# Create your models here.
from Ratatoskr.anotations import handler


class Movie(models.Model):
    @handler(method="nameLIKE")
    def handleLIKE(self, data):
        tmp = Movie.objects.filter(name__contains=data["name"])
        return list(map(lambda x: x.id, tmp))

    name = models.TextField()
    year = models.IntegerField()
    image = models.TextField()

    def JSON(self):
        return {
            "name": self.name,
            "pk": self.pk,
            "year": self.year,
            "image": self.image
        }

    class Nuts:
        public = {'pk', 'name', 'year', 'image'}
        index_by = 'pk'

        assert (index_by in public)
