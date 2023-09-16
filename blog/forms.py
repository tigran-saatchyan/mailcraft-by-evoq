from django import forms

from blog.models import Posts
from frontend.forms import StyleFormMixin

PROHIBITED_WORDS = []

def validate_prohibited_words(clean_data):
    """
    Validate if any prohibited words are used in the input data.

    Args:
        clean_data (str): The input data to be validated.

    Raises:
        forms.ValidationError: If any prohibited words are found in the input data.
    """
    for word in PROHIBITED_WORDS:
        if word.lower() in clean_data.lower():
            raise forms.ValidationError(
                'Вы использовали одно из запрещённых слов: \n'
                f'{", ".join(PROHIBITED_WORDS)}'
            )

class PostForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and updating blog posts.

    This form is used to create and update blog posts, including specifying the title, content, image, and publication status.

    Attributes:
        clean_title (method): Custom validation for the title field to check for prohibited words.
        clean_content (method): Custom validation for the content field to check for prohibited words.

        Meta (class): A class that specifies the associated model (Posts) and the fields to display in the form.
    """
    def clean_title(self):
        """
        Custom validation for the title field to check for prohibited words.

        Returns:
            str: The cleaned title data.

        Raises:
            forms.ValidationError: If any prohibited words are found in the title.
        """
        clean_data = self.cleaned_data['title']
        validate_prohibited_words(clean_data)
        return clean_data

    def clean_content(self):
        """
        Custom validation for the content field to check for prohibited words.

        Returns:
            str: The cleaned content data.

        Raises:
            forms.ValidationError: If any prohibited words are found in the content.
        """
        clean_data = self.cleaned_data['content']
        validate_prohibited_words(clean_data)
        return clean_data

    class Meta:
        model = Posts
        fields = ('title', 'content', 'image', 'is_published')
