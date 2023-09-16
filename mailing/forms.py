from django import forms
from frontend.forms import StyleFormMixin
from mailing.models import Mailing, MailingSettings


class MailingForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and updating mailing settings.

    This form is used to create and update mailing settings, including specifying the title, message title, message content, and contact list.

    Attributes:
        Meta (class): A class that specifies the associated model (Mailing) and the fields to display in the form.

    """

    class Meta:
        model = Mailing
        fields = (
            'title',
            'message_title',
            'message_content',
            'contact_list',
        )


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and updating mailing schedule settings.

    This form is used to create and update mailing schedule settings, including specifying the mailing, mailing periods, status, start date, mailing time, mailing week day number, and end date.

    Attributes:
        Meta (class): A class that specifies the associated model (MailingSettings) and the fields to display in the form.

    """

    class Meta:
        model = MailingSettings
        fields = (
            'mailing',
            'mailing_periods',
            'status',
            'start_date',
            'mailing_time',
            'mailing_week_day_num',
            'end_date',
        )

        widgets = {
            'mailing_time': forms.TimeInput(
                format="%H:%M",
                attrs={
                    'type': 'time',
                }
            ),
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }


class DetailForm(forms.ModelForm):
    """
    Form for displaying mailing details.

    This form is used to display mailing details, including the title, message title, message content, and mailing time.

    Attributes:
        Meta (class): A class that specifies the associated model (Mailing) and the fields to display in the form.

    """

    class Meta:
        model = Mailing
        fields = (
            'title',
            'message_title',
            'message_content',
        )
        widgets = {
            'mailing_time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }
