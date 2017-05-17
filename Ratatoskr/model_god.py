import inspect

from django.contrib import admin
from django.db import models

from django.template.backends import django


class ModelGod:
    @staticmethod
    def getHandleFunction(model, data, method):
        handler = ModelGod.get_handler(data, method, model)
        return handler

    @staticmethod
    def get_model(app_name, model_name):
        registered_apps = django.apps
        for app in registered_apps.all_models:
            if app == app_name:
                tmp = django.apps.all_models.get(app)
                for _model in tmp:
                    if _model == str.lower(model_name):
                        return registered_apps.get_model(app_label=app, model_name=_model)
        return None

    @staticmethod
    def get_handler(data, method, model):
        if model is not  None:
            for attr in model.__dict__:
                possibleHandler = model.__dict__[attr]
                if (hasattr(possibleHandler, '__ratamethod__')):
                    if possibleHandler.__ratamethod__ == method:
                        return possibleHandler
        return None

