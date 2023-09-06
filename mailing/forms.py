from django import forms

from frontend.forms import StyleFormMixin
from mailing.models import Mailing


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = (
            'title',
            'mailing_time',
            'mailing_periods',
            'status',
            'message_title',
            'message_content',
        )
        widgets = {
            'mailing_time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }


class DetailForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = (
            'title',
            'mailing_time',
            'mailing_periods',
            'status',
            'message_title',
            'message_content',
        )
        widgets = {
            'mailing_time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }
