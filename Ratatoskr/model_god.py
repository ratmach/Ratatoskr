import inspect

from django.template.backends import django


class ModelGod:
    @staticmethod
    def getHandleFunction(app_name, model_name, data, method):
        registered_apps = django.apps
        print("did it ")
        for app in registered_apps.all_models:
            if app == app_name:
                tmp = django.apps.all_models.get(app)
                for model in tmp:
                    if model == str.lower(model_name):
                        model = registered_apps.get_model(app_label=app, model_name=model)
                        for attr in model.__dict__:
                            possibleHandler = model.__dict__[attr]
                            if (hasattr(possibleHandler, '__ratamethod__')):
                                if possibleHandler.__ratamethod__ == method:
                                    possibleHandler(None,data)

        pass
