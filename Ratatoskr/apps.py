from django.apps import AppConfig
from django.template.backends import django


class RatatoskrGenerator(AppConfig):
    name = 'Ratatoskr'
    defaultModelMarkup = "Ratatoskr/defaultModel.js"
    destionation = 'static/js'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        tmp = []
        with open(RatatoskrGenerator.defaultModelMarkup, "r") as f:
            tmp = f.readlines()
        self.template = "".join(tmp)

    def ready(self):
        print("Ratatoskr is collecting nuts")
        registered_apps = self.apps.all_models
        for apps in registered_apps:
            tmp = django.apps.all_models.get(apps)
            for model in tmp:
                model = self.apps.get_model(app_label=apps, model_name=model)
                if "Nuts" in model.__dict__:
                    print("Found nut in: {0}.".format(apps, model))
                    self.generateJS(model, model.Nuts)

    def generateJS(self, model, nut):
        print(nut.public)
        nutSet = set(nut.public)
        arguments = []
        for variable in model._meta.fields:
            if variable.attname in nutSet:
                arguments.append(variable.attname)
                print("variable:{0} of type: {1}, with default of {2}, can be null: {3}, isUnique: {4}".format(
                    variable, type(variable), variable.default, variable.null, variable.unique
                ))

        print(self.getPrototype(model._meta.object_name, arguments))

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

    def getPrototypeAssignment(self, arguments):
        out = []
        for argument in arguments:
            out.append("this.")
            out.append(argument)
            out.append("=")
            out.append(argument)
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
