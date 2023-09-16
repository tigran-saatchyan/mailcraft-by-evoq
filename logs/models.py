from django.db import models

from mailing.models import Mailing

# Define a dictionary for fields that can be nullable
NULLABLE = {'blank': True, 'null': True}


class Logging(models.Model):
    """
    Model for logging mailing attempts.

    This model is used to log the attempts made for a mailing, including the status of the attempt and the timestamp of the last attempt.

    Attributes:
        ATTEMPT_OK (str): Constant for a successful attempt.
        ATTEMPT_ERROR (str): Constant for an unsuccessful attempt.
        ATTEMPT_STATUS (tuple): Choices for the attempt status field.

        last_attempt (DateTimeField): The timestamp of the last attempt (auto-generated).
        mailing (ForeignKey): The related mailing for the attempt.
        attempt_status (CharField): The status of the attempt (successful or unsuccessful).

    Methods:
        __str__: String representation of the logging entry.

    Meta:
        verbose_name (str): The singular name of the model.
        verbose_name_plural (str): The plural name of the model.
    """
    ATTEMPT_OK = 'ok'
    ATTEMPT_ERROR = 'error'

    ATTEMPT_STATUS = (
        (ATTEMPT_OK, 'Удачная попытка'),
        (ATTEMPT_ERROR, 'Неудачная попытка')
    )

    last_attempt = models.DateTimeField(
        auto_now_add=True, verbose_name='последня попытка'
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='рассылка',
        **NULLABLE
    )
    attempt_status = models.CharField(
        max_length=50,
        choices=ATTEMPT_STATUS,
        verbose_name='статус попытки',
        **NULLABLE
    )

    def __str__(self):
        """
        String representation of the logging entry.

        Returns:
            str: The title of the associated mailing.

        """
        return f'{self.mailing.title}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'настройки рассылок'
