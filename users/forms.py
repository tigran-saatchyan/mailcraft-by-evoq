from django.contrib.auth.forms import (
    PasswordChangeForm as BasePasswordChangeForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm,
    UserChangeForm as BaseUserChangeForm,
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import HiddenInput

from frontend.forms import StyleFormMixin
from users.models import User

class RegisterForm(StyleFormMixin, UserCreationForm):
    """
    A form for user registration.

    Inherits from UserCreationForm and includes styling.

    Args:
        UserCreationForm: The base class for user registration.

    Returns:
        None
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class LoginForm(StyleFormMixin, AuthenticationForm):
    """
    A form for user login.

    Inherits from AuthenticationForm and includes styling.

    Args:
        AuthenticationForm: The base class for user login.

    Returns:
        None
    """

    class Meta:
        model = User
        fields = ('__all__',)


class UserChangeForm(StyleFormMixin, BaseUserChangeForm):
    """
    A form for user profile updates.

    Inherits from UserChangeForm and includes styling.

    Args:
        BaseUserChangeForm: The base class for user profile updates.

    Returns:
        None
    """

    class Meta:
        model = User
        fields = (
            'avatar',
            'email',
            'password',
            'first_name',
            'last_name',
            'telephone',
            'country',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()


class PasswordResetForm(StyleFormMixin, BasePasswordResetForm):
    """
    A form for resetting a user's password.

    Inherits from PasswordResetForm and includes styling.

    Args:
        BasePasswordResetForm: The base class for password reset.

    Returns:
        None
    """

    email_template_name = 'users/registration/password_reset_email.html'


class SetPasswordForm(StyleFormMixin, BaseSetPasswordForm):
    """
    A form for setting a new user password.

    Inherits from SetPasswordForm and includes styling.

    Args:
        BaseSetPasswordForm: The base class for setting a new password.

    Returns:
        None
    """

    class Meta:
        model = User
        fields = ('__all__',)


class PasswordChangeForm(BasePasswordChangeForm):
    """
    A form for changing a user's password.

    Inherits from PasswordChangeForm.

    Args:
        BasePasswordChangeForm: The base class for changing a password.

    Returns:
        None
    """
    pass
