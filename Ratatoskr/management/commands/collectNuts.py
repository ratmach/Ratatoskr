from django.core.management import BaseCommand
from django.template.backends import django


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("--CollectNutsFor", nargs='+')
        parser.add_argument("--CollectNuts", action='store_true')
        parser.add_argument("--ListModels", action='store_true')

    def handle(self, *args, **options):
        models = django.apps.all_models.keys()
        if options["ListModels"]:
            for i in models:
                self.stdout.write(i)
        if options["CollectNuts"]:
            pass
        if options["CollectNutsFor"]:
            pass