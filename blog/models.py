from django.db import models

from service.utils import save_picture
from users.models import User

class Posts(models.Model):
    """
    Model for representing blog posts.

    Attributes:
        title (str): The title of the post.
        slug (str): The slug for the post.
        content (str): The content of the post.
        image (ImageField): The image associated with the post.
        creation_date (DateTimeField): The date and time of post creation.
        is_published (bool): A flag indicating if the post is published.
        views_count (int): The number of views the post has received.
        user (ForeignKey): The user who created the post.

    Methods:
        __str__: String representation of the post.

    Meta:
        verbose_name (str): The singular name of the model.
        verbose_name_plural (str): The plural name of the model.
        ordering (tuple): The default ordering for the posts.
    """
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(blank=True, verbose_name='контент')
    image = models.ImageField(
        upload_to=save_picture,
        blank=True,
        verbose_name='изображение'
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='опубликован'
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name='просмотры'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )

    def __str__(self):
        """
        String representation of the post.

        Returns:
            str: The title of the post.
        """
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('creation_date',)
