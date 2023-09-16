from datetime import datetime
from typing import Dict

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from service.utils import save_picture

NULLABLE: Dict[str, bool] = {'blank': True, 'null': True}


class Country(models.Model):
    """
    A model representing a country.

    Args:
        models.Model: The base class for defining a Django model.

    Attributes:
        name (str): The name of the country.
        code (str): The code or abbreviation of the country.

    Meta:
        verbose_name (str): A human-readable name for the model.
        verbose_name_plural (str): A human-readable plural name for the model.
        ordering (tuple): The default ordering for instances of this model.

    Methods:
        __str__(): Returns a string representation of the country.

    Returns:
        None
    """

    name = models.CharField(max_length=255, **NULLABLE, verbose_name='страна')
    code = models.CharField(max_length=255, **NULLABLE, verbose_name='код')

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'


class User(AbstractUser):
    """
    A custom user model extending Django's AbstractUser.

    Args:
        AbstractUser: The base class for defining a custom user model.

    Attributes:
        email (str): The unique email address of the user.
        telephone (str): The user's telephone number.
        country (Country): The user's country of residence.
        avatar (ImageField): The user's profile picture.
        date_added (datetime): The date and time when the user account was created.
        last_modified (datetime): The date and time when the user account was last modified.
        is_verified (bool): A flag indicating whether the user's email is verified.

    Meta:
        verbose_name (str): A human-readable name for the model.
        verbose_name_plural (str): A human-readable plural name for the model.
        ordering (tuple): The default ordering for instances of this model.

    Methods:
        __str__(): Returns a string representation of the user.

    Returns:
        None
    """

    username = None
    email = models.EmailField(
        unique=True, verbose_name='почта', validators=[
            validators.EmailValidator(message="Invalid Email")
        ]
    )
    telephone = models.CharField(
        max_length=50, verbose_name='телефон', **NULLABLE
    )
    country = models.ForeignKey(
        Country,
        verbose_name='страна',
        on_delete=models.CASCADE,
        max_length=255,
        **NULLABLE,
    )
    avatar = models.ImageField(upload_to=save_picture, **NULLABLE)
    date_added: datetime = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    last_modified: datetime = models.DateTimeField(
        verbose_name='последнее изменение',
        auto_now=True
    )

    is_verified: bool = models.BooleanField(
        verbose_name='статус верификации',
        default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('date_added',)
