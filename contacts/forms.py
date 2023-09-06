from django import forms

from contacts.models import Contacts, Lists
from frontend.forms import StyleFormMixin


class ContactForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'


class ListForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Lists
        fields = '__all__'
