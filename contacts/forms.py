from django import forms

from contacts.models import Contacts, Lists
from frontend.forms import StyleFormMixin


class ContactForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and updating contact information.

    This form is used to create and update contact information, including telephone number, email, and status.

    Attributes:
        Meta (class): A class that specifies the associated model (Contacts) and the fields to display in the form.

    """

    class Meta:
        model = Contacts
        fields = (
            'telephone',
            'email',
            'status',
            'list'
        )


class ListForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and updating contact lists.

    This form is used to create and update contact lists, including specifying the user who owns the list.

    Attributes:
        Meta (class): A class that specifies the associated model (Lists) and includes all fields except 'user'.

    """

    class Meta:
        model = Lists
        fields = '__all__'
        exclude = ('user',)
