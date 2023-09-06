from django.db import models

from contacts.models import Contacts
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class MailingStatuses(models.Model):
    status = models.CharField(
        max_length=20,
        verbose_name='статус рассылки'
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'статус рассылки'
        verbose_name_plural = 'статусы рассылок'


class MailingPeriods(models.Model):
    period_name = models.CharField(max_length=100, **NULLABLE)
    cron_setting = models.CharField(max_length=255, **NULLABLE)

    def __str__(self):
        return self.period_name

    class Meta:
        verbose_name = 'период рассылки'
        verbose_name_plural = 'период рассылок'


class Mailing(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название рассылки',
        **NULLABLE
    )
    mailing_time = models.TimeField(
        verbose_name='время рассылки',
        **NULLABLE
    )
    mailing_periods = models.ForeignKey(
        MailingPeriods,
        on_delete=models.SET_NULL,
        **NULLABLE
    )
    status = models.ForeignKey(
        MailingStatuses,
        on_delete=models.DO_NOTHING,
        default=2,
        verbose_name='статус рассылки',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        **NULLABLE
    )
    message_title = models.CharField(max_length=255, **NULLABLE)
    message_content = models.TextField(**NULLABLE)

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='дата изменения'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
