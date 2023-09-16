import json
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Custom management command for loading initial countries from a JSON file.
    """
    help = 'Load initial countries from a JSON file'

    def handle(self, *args, **options):
        """
        Handle the command execution.

        This function reads a JSON file containing country data and loads it into the database.
        It first retrieves the path to the JSON file and then iterates over the data to create
        Country objects in the database.

        Args:
            *args: Additional command arguments (not used).
            **options: Additional keyword arguments (not used).

        Returns:
            None

        Example:
            To load initial countries from the JSON file, run:
            $ python manage.py load_countries
        """
        static_url = settings.STATICFILES_DIRS[0]
        filename = Path(static_url, 'users/data/countries.json')

        with open(filename, 'r') as json_file:
            countries_data = json.load(json_file)
            Country = apps.get_model('users', 'Country')
            for country_data in countries_data:
                Country.objects.create(
                    name=country_data['name'],
                    code=country_data['code']
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial countries')
        )
