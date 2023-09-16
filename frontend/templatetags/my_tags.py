from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def media_path(path):
    """
    Custom Django template filter for converting a relative media path
    to an absolute URL.

    Args:
        path (str): The relative path to a media file.

    Returns:
        str: The absolute URL to the media file.

    Example:
        In a Django template, you can use this filter like this:
        {{ 'uploads/my_image.jpg' | media_path }}
        This will output the absolute URL to the 'my_image.jpg' file
        in the media root.
    """
    from django.conf import settings

    media_url = settings.MEDIA_URL

    return f'{media_url}{path}'
