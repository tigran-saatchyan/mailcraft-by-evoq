from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Custom Django management command to load sample data into the database.

    Usage: python manage.py load_sample_data

    This command loads data from a predefined fixture file
    'mailcraft_data.json' into the database.
    """

    help = 'Load sample data into the database'

    def handle(self, *args, **options):
        """
        Handles the execution of the 'load_demo_data' management command.

        Args:
            *args: Additional command-line arguments.
            **options: Additional command options.

        Example:
            To load sample data, run:
            python manage.py load_demo_data
        """
        call_command('loaddata', 'static/mailcraft_data.json')
