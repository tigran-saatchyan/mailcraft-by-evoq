from django.core.management import BaseCommand

from mailing.cron import run_mailing


class Command(BaseCommand):
    """
    Custom management command for sending scheduled mailings.
    """
    help = 'Send scheduled mailings.'

    def add_arguments(self, parser):
        """
        Define command-line arguments for the management command.

        Args:
            parser (argparse.ArgumentParser): The ArgumentParser instance.

        Returns:
            None

        Example:
            To use this command, run:
            $ python manage.py send_scheduled_mailings <mailing_pk>
        """
        parser.add_argument(
            'mailing_pk', type=str, help='PK of the mailing to be sent'
            )

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.

        This function takes the primary key (PK) of a mailing as an
        argument and triggers the sending of the scheduled mailing
        using the `run_mailing` function.

        Args:
            *args: Additional command arguments (not used).
            **kwargs: Additional keyword arguments, including 'mailing_pk'
                (the PK of the mailing).

        Returns:
            None

        Example:
            To send a scheduled mailing with a specific PK, run:
            $ python manage.py send_scheduled_mailings <mailing_pk>
        """
        mailing_pk = kwargs['mailing_pk']
        run_mailing(mailing_pk)
