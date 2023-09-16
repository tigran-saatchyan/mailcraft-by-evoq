import re
from datetime import datetime

from django.core.mail import send_mail


def save_picture(instance, filename):
    """
    Generate a unique filename for saving a picture associated with an instance.

    Args:
        instance: The instance (e.g., a model instance) for which the picture is being saved.
        filename (str): The original filename of the picture.

    Returns:
        str: The unique filename for saving the picture.
    """
    app_name = instance._meta.app_label
    model_name = instance._meta.model_name
    my_date = str(datetime.now().isoformat())

    picture_name = "".join(
        [
            "".join(filename.split('.')[:-1]),
            my_date,
            ".",
            filename.split('.')[-1]
        ]
    )
    return f"{app_name}/{model_name}/{instance.pk}/{instance.pk}_{picture_name}"


def view_counter_email_notification(views_count, title):
    """
    Send an email notification when a post reaches a specific view count.

    Args:
        views_count (int): The current view count of the post.
        title (str): The title of the post.

    Returns:
        None
    """
    if views_count == 100:
        subject = f'Congratulations!'
        message = f'<p>The post "{title}" has reached ' \
                  f'100 views.</p>'
        email = 'mr.saatchyan@yandex.com'

        send_mail(
            subject=subject,
            from_email=None,
            recipient_list=[email],
            message=message
        )


def validate_email_address(email_address):
    """
    Validate an email address for basic format compliance.

    This function checks if the given email address follows a basic format:
    - It contains only valid characters including letters, numbers, and
        certain special characters.
    - It has the "@" symbol followed by a domain name.

    Args:
        email_address (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    if not re.search(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            email_address
    ):
        print(f"The email address {email_address} is not valid")
        return False
    return True
