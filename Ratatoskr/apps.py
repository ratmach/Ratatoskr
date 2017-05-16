import os

from django.apps import AppConfig
from django.template.backends import django
from django.db.models.fields import NOT_PROVIDED, CharField, TextField, EmailField, DateTimeField, IntegerField, FloatField


class RatatoskrGenerator(AppConfig):
    name = 'Ratatoskr'
    defaultModelMarkup = "Ratatoskr/defaultModel.Ratatoskr"
    destionation = 'static/js'
    apps = {}

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        tmp = []
        with open(RatatoskrGenerator.defaultModelMarkup, "r") as f:
            tmp = f.readlines()
        self.template = "".join(tmp)


    def ready(self):
        print("Ratatoskr is collecting nuts")
        registered_apps = self.apps.all_models

        RatatoskrGenerator.apps = self.apps
        for apps in registered_apps:
            tmp = django.apps.all_models.get(apps)
            for model in tmp:
                model = self.apps.get_model(app_label=apps, model_name=model)
                if "Nuts" in model.__dict__:
                    print("Found nut in: {0}.".format(apps, model))
                    with open(os.path.join(RatatoskrGenerator.destionation, "".join([model._meta.object_name, ".js"])),
                              "w") as f:
                        f.write(self.generateJS(model, model.Nuts))
                        f.flush()

    def generateJS(self, model, nut):
        print(nut.public)
        nutSet = set(nut.public)
        arguments = {}
        for variable in model._meta.fields:
            if variable.attname in nutSet:
                arguments[variable.attname] = {
                    "type": type(variable),
                    "null": variable.null,
                    "unique": variable.unique
                }
                if type(variable.default) != type(NOT_PROVIDED):
                    arguments[variable.attname]["default"] = variable.default

        return self.getPrototype(model._meta.object_name, arguments)

    def getPrototype(self, name, arguments):
        return self.template.format(name, self.getArgumentsList(arguments), self.getPrototypeAssignment(arguments),
                                    self.getUpdateFunction(name, arguments),
                                    self.getCreateFunction(name, arguments),
                                    self.getDeleteFunction(name, arguments), self.getGetFunction(name, arguments),
                                    self.getCheckSetRules(name, arguments))

    def getArgumentsList(self, arguments):
        out = []
        for argument in arguments:
            out.append(argument)
        return ",".join(out)

    def formatByType(self, value, type_):
        if type(type_) == type(CharField) or type(type_) == type(TextField) or type(type_) == EmailField:
            return "\"" + str(value) + "\""
        return value

    def getPrototypeAssignment(self, arguments):
        out = []
        for argument in arguments:
            out.append("this.")
            out.append(argument)
            out.append("=")
            out.append(argument)
            if "default" in arguments[argument]:
                out.append(" || ")
                tmp = self.formatByType(arguments[argument]["default"], arguments[argument]["type"])
                out.append(tmp)
            out.append(";")
        return "".join(out)

    def getUpdateFunction(self, name, arguments):
        return "undefined"

    def getCreateFunction(self, name, arguments):
        return "undefined"

    def getDeleteFunction(self, name, arguments):
        return "undefined"

    def getGetFunction(self, name, arguments):
        return "undefined"

    def getCheckSetRules(self, name, arguments):
        return "undefined"
