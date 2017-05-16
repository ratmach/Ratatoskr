from django.apps import AppConfig
from django.template.backends import django


class RatatoskrGenerator(AppConfig):
    name = 'Ratatoskr'
    destionation = 'static/js'

    def ready(self):
        print("Ratatoskr is collecting nuts")
        registered_apps = self.apps.all_models
        for apps in registered_apps:
            tmp = django.apps.all_models.get(apps)
            for model in tmp:
                model = self.apps.get_model(app_label=apps, model_name=model)
                if "Nuts" in model.__dict__:
                    print("Found nut in: {0}.".format(apps,model))
                    self.generateJS(model, model.Nuts)

    def generateJS(self, model, nut):
        print(nut.public)
        nutSet = set(nut.public)
        for variable in model._meta.fields:
            if variable.attname in nutSet:
                print("variable:{0} of type: {1}, with default of {2}, can be null: {3}, isUnique: {4}".format(
                    variable,  type(variable), variable.default, variable.null, variable.unique
                ))