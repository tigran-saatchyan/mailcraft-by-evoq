from django.db import models

from contacts.models import Contacts, ContactsList, Lists
from users.models import User

# Define a dictionary for fields that can be nullable
NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """
    Model for representing mailing settings.

    This model represents mailing settings, including the title, author, message title, message content, date created, date modified, mailing settings, and contact list.

    Attributes:
        title (CharField): The title of the mailing.
        user (ForeignKey): The author of the mailing.
        message_title (CharField): The message title of the mailing.
        message_content (TextField): The message content of the mailing.
        date_created (DateTimeField): The timestamp of when the mailing was created (auto-generated).
        date_modified (DateTimeField): The timestamp of when the mailing was last modified (auto-updated).
        setting (OneToOneField): The related mailing settings.
        contact_list (ForeignKey): The related contact list for the mailing.

    Methods:
        __str__: String representation of the mailing.

    Meta:
        verbose_name (str): The singular name of the model.
        verbose_name_plural (str): The plural name of the model.
    """
    title = models.CharField(
        max_length=255,
        verbose_name='название рассылки',
        **NULLABLE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        **NULLABLE
    )
    message_title = models.CharField(
        max_length=255,
        verbose_name='тема сообщения',
        **NULLABLE
    )
    message_content = models.TextField(
        **NULLABLE,
        verbose_name='сообщение',
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='дата изменения'
    )

    setting = models.OneToOneField(
        'MailingSettings',
        on_delete=models.SET_NULL,
        related_name='mailing_settings',
        **NULLABLE,
        verbose_name='настройки рассылки'
    )
    contact_list = models.ForeignKey(
        Lists,
        on_delete=models.CASCADE,
        verbose_name='Списки контактов',
        **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingSettings(models.Model):
    """
    Model for representing mailing settings.

    This model represents mailing settings, including the mailing, mailing periods, status, start date, mailing time, mailing week day number, end date, and cron settings.

    Attributes:
        mailing (OneToOneField): The related mailing.
        mailing_periods (CharField): The periodicity of the mailing (daily, weekly, monthly).
        status (CharField): The status of the mailing (new, running, completed).
        start_date (DateField): The start date of the mailing.
        mailing_time (TimeField): The time of day for the mailing.
        mailing_week_day_num (IntegerField): The day of the week for the mailing.
        end_date (DateField): The end date of the mailing.
        cron_setting (TextField): The CRON settings for the mailing.

    Methods:
        __str__: String representation of the mailing settings.

    Meta:
        verbose_name (str): The singular name of the model.
        verbose_name_plural (str): The plural name of the model.
    """
    MAILING_DAILY = 'daily'
    MAILING_WEEKLY = 'weekly'
    MAILING_MONTHLY = 'monthly'

    MAILING_PERIODS = (
        (MAILING_DAILY, 'Раз в день'),
        (MAILING_WEEKLY, 'Раз в неделю'),
        (MAILING_MONTHLY, 'Раз в месяц')
    )

    MAILING_NEW = 'new'
    MAILING_RUNNING = 'running'
    MAILING_COMPLETED = 'completed'

    MAILING_STATUSES = (
        (MAILING_NEW, 'новая'),
        (MAILING_RUNNING, 'запущена'),
        (MAILING_COMPLETED, 'завершена'),
    )

    mailing = models.OneToOneField(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='рассылка',
        **NULLABLE,
    )
    mailing_periods = models.CharField(
        max_length=50,
        choices=MAILING_PERIODS,
        verbose_name='периодичность рассылки',
        **NULLABLE,
    )
    status = models.CharField(
        max_length=50,
        choices=MAILING_STATUSES,
        verbose_name='статус рассылки',
        **NULLABLE,
    )
    start_date = models.DateField(
        **NULLABLE,
        verbose_name='дата начала'
    )
    mailing_time = models.TimeField(
        verbose_name='время рассылки',
        **NULLABLE
    )
    mailing_week_day_num = models.IntegerField(
        verbose_name='день недели',
        **NULLABLE,
    )

    end_date = models.DateField(
        **NULLABLE,
        verbose_name='дата окончания'
    )
    cron_setting = models.TextField(
        **NULLABLE,
        verbose_name='настройка CRON'
    )

    def __str__(self):
        return f'{self.mailing.title}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'настройки рассылок'
