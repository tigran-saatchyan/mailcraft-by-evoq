from django import forms


class StyleFormMixin:
    """
    Mixin class for styling form fields.

    This mixin automatically adds the 'form-control' class to all form fields, except for checkbox inputs,
    to apply styling to the form fields in HTML templates.

    Methods:
        __init__: Constructor method that applies the 'form-control' class to form fields.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method that applies the 'form-control' class to form fields.

        Args:
            *args: Positional arguments passed to the constructor.
            **kwargs: Keyword arguments passed to the constructor.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
