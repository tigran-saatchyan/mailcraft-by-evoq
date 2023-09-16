from django.core.management import BaseCommand

from service.utils import validate_email_address
from users.models import User


class Command(BaseCommand):
    """
    Custom management command for creating a superuser with admin privileges.
    """
    help = 'Create a superuser with admin privileges.'

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.

        This function guides the user through the process of creating a
        superuser with admin privileges. It prompts for an email address,
        first name, last name, and password. The email address is validated
        using the `validate_email_address` function. If the email address is
        valid and passwords match, a superuser is created with the
        provided information.

        Args:
            *args: Additional command arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            None

        Example:
            To create a superuser with admin privileges, run:
            $ python manage.py create_superuser
        """
        email = input('Enter admin e-mail (required): ')
        is_valid_email = validate_email_address(email)

        if not is_valid_email:
            self.stderr.write(
                self.style.ERROR(
                    f'Email "{email}" is not a valid email address. '
                    f'Superuser creation failed.'
                )
            )
            return

        first_name = input('Enter your first name: ')
        last_name = input('Enter your last name: ')
        password1 = input('Enter your password (required): ')
        password2 = input('Repeat your password (required): ')

        if password1 != password2:
            self.stderr.write(
                self.style.ERROR(
                    'Passwords do not match. Superuser creation failed.'
                )
            )
            return

        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(password2)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'SuperUser {user.email} created\n'
                f'Welcome to EvoQ Family Club {first_name} {last_name}'
            )
        )
