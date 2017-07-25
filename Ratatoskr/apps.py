import os

from django.apps import AppConfig
from django.db import transaction
from django.template.backends import django
from django.db.models.fields import NOT_PROVIDED, CharField, TextField, EmailField, DateTimeField, IntegerField, \
    FloatField

from ratExample.consumers import messageToSubscribed


class RatatoskrGenerator(AppConfig):
    socketPath = "chat"

    name = 'Ratatoskr'

    defaultModelMarkup = "Ratatoskr/scriptTemplates/defaultModel.Ratatoskr"

    defaultGetFunctionMarkup = "Ratatoskr/scriptTemplates/defaultGetFunction.Ratatoskr"
    defaultUpdateFunctionMarkup = "Ratatoskr/scriptTemplates/defaultUpdateFunction.Ratatoskr"
    defaultCreateFunctionMarkup = "Ratatoskr/scriptTemplates/defaultCreateFunction.Ratatoskr"
    defaultDeleteFunctionMarkup = "Ratatoskr/scriptTemplates/defaultDeleteFunction.Ratatoskr"

    destination = 'static/js'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        tmp = []
        with open(RatatoskrGenerator.defaultModelMarkup, "r") as f:
            tmp = f.readlines()
        self.template = "".join(tmp)

        tmp = []
        with open(RatatoskrGenerator.defaultGetFunctionMarkup, "r") as f:
            tmp = f.readlines()
        self.getTemplate = "".join(tmp)
        tmp = []
        with open(RatatoskrGenerator.defaultCreateFunctionMarkup, "r") as f:
            tmp = f.readlines()
        self.createTemplate = "".join(tmp)
        with open(RatatoskrGenerator.defaultUpdateFunctionMarkup, "r") as f:
            tmp = f.readlines()
        self.updateTemplate = "".join(tmp)
        with open(RatatoskrGenerator.defaultDeleteFunctionMarkup, "r") as f:
            tmp = f.readlines()
        self.deleteTemplate = "".join(tmp)

    def ready(self):
        print("Ratatoskr is collecting nuts")
        registered_apps = self.apps.all_models
        for apps in registered_apps:
            tmp = django.apps.all_models.get(apps)
            for model in tmp:
                model = self.apps.get_model(app_label=apps, model_name=model)
                if "Nuts" in model.__dict__ and "ignore_flag" not in model.Nuts.__dict__:
                    oldsave = model.save

                    def savef(self, *args, **kwargs):
                        try:
                            with transaction.atomic():
                                oldsave(self, *args, **kwargs)
                            messageToSubscribed(self._meta.label, self.JSON())
                        except Exception as e:
                            print(e)
                            pass

                    model.save = savef
                    print("Found nut in: {0}.".format(apps, model))
                    with open(os.path.join(RatatoskrGenerator.destination, "".join([model._meta.object_name, ".js"])),
                              "w") as f:
                        f.write(self.generateJS(model, model.Nuts, apps))
                        f.flush()

    def generateJS(self, model, nut, app):
        print(nut.public)
        nutSet = set(nut.public)
        index_by = nut.index_by
        arguments = {}
        fields = sorted(model._meta.fields)
        for variable in model._meta.fields:
            if variable.attname in nutSet:
                arguments[variable.attname] = {
                    "type": type(variable),
                    "null": variable.null,
                    "unique": variable.unique
                }
                if type(variable.default) != type(NOT_PROVIDED):
                    arguments[variable.attname]["default"] = variable.default

        return self.getPrototype(model._meta.object_name, arguments, app, index_by)

    def getPrototype(self, name, arguments, app, index_by):
        return self.template.format(name, self.getArgumentsList(arguments), self.getPrototypeAssignment(arguments),
                                    self.getUpdateFunction(name, app),
                                    self.getCreateFunction(name, app),
                                    self.getDeleteFunction(name, app),
                                    self.getGetFunction(name, app, index_by),
                                    self.getCheckSetRules(name, arguments),
                                    ".".join([app, name]))

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

    def getUpdateFunction(self, name, app):
        return self.updateTemplate.format(app, name)

    def getCreateFunction(self, name, app):
        return self.createTemplate.format(app, name)

    def getDeleteFunction(self, name, app):
        return self.deleteTemplate.format(app, name)

    def getGetFunction(self, name, app, index_by):
        return self.getTemplate.format(app, name, index_by)

    def getCheckSetRules(self, name, arguments):
        return "undefined"
