from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import (
    PasswordChangeDoneView as BasePasswordChangeDoneView
)
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView
)
from django.contrib.auth.views import (
    PasswordResetCompleteView as BasePasswordResetCompleteView
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib.auth.views import (
    PasswordResetDoneView as BasePasswordResetDoneView
)
from django.contrib.auth.views import (
    PasswordResetView as BasePasswordResetView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from users.forms import RegisterForm, LoginForm, UserChangeForm, \
    PasswordResetForm, PasswordChangeForm, SetPasswordForm
from users.models import User


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for password reset.

    This class generates a unique token for resetting a user's password.

    Methods:
        _make_hash_value(self, user, timestamp): Generates a hash value for the token.

    Attributes:
        None

    Returns:
        None
    """
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_active)
        )


generate_token = TokenGenerator()


class RegisterView(CreateView):
    """
    User registration view.

    This view allows users to register by providing their email and password.

    Methods:
        send_verification_email(self, user): Sends a verification email to the user.
        form_valid(self, form): Handles a valid form submission.

    Attributes:
        model: The User model.
        form_class: The form class to use for user registration.
        success_url: The URL to redirect to upon successful registration.
    """

    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')

    def send_verification_email(self, user):
        """
        Sends a verification email to the user.

        Args:
            user: The user to send the email to.

        Returns:
            None
        """
        token = generate_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Подтверждение электронной почты'
        message = render_to_string(
            'users/registration/verification_email.html',
            {
                'user': user,
                'uid': uid,
                'domain': current_site.domain,
                'token': token
            }
        )

        send_mail(
            subject=mail_subject,
            message=message,
            from_email=None,
            recipient_list=[user.email],
            html_message=message
        )

    def form_valid(self, form):
        self.object = form.save()
        self.send_verification_email(self.object)
        return super().form_valid(form)


def verify_email(request, uidb64, token):
    """
    Verify user's email based on the provided token.

    Args:
        request: The HTTP request object.
        uidb64: The user's ID encoded in base64.
        token: The verification token.

    Returns:
        None
    """
    data = {}
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(
            user, token
    ):
        user.is_verified = True
        user.is_active = True
        user.save()
        data['user'] = user

        return render(
            request,
            'users/registration/email_verified.html',
            context=data
        )

    return render(
        request,
        'users/registration/email_verified.html',
        context=data
    )


class LoginView(BaseLoginView):
    """
    User login view.

    This view allows users to log in to their accounts.

    Methods:
        None

    Attributes:
        form_class: The form class to use for user login.
    """
    form_class = LoginForm


class LogoutView(BaseLogoutView):
    """
    User logout view.

    This view allows users to log out of their accounts.

    Methods:
        None

    Attributes:
        None
    """
    pass


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    User profile update view.

    This view allows users to update their profile information.

    Methods:
        get_object(self, queryset=None): Retrieves the user object to update.

    Attributes:
        model: The User model.
        success_url: The URL to redirect to upon successful profile update.
        form_class: The form class to use for profile update.
    """
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserChangeForm

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(BasePasswordResetView):
    """
    Password reset view.

    This view allows users to request a password reset via email.

    Methods:
        None

    Attributes:
        model: The User model.
        form_class: The form class to use for password reset.
        email_template_name: The name of the email template.
        success_url: The URL to redirect to upon successful password reset request.
    """
    model = User
    form_class = PasswordResetForm
    email_template_name = 'users/registration/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetDoneView(BasePasswordResetDoneView):
    """
    Password reset done view.

    This view is displayed after a successful password reset request.

    Methods:
        None

    Attributes:
        None
    """
    pass


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    """
    Password reset confirmation view.

    This view allows users to reset their password using a confirmation link.

    Methods:
        None

    Attributes:
        form_class: The form class to use for password reset confirmation.
        success_url: The URL to redirect to upon successful password reset.
    """
    form_class = SetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    """
    Password reset complete view.

    This view is displayed after a successful password reset.

    Methods:
        None

    Attributes:
        None
    """
    pass


class PasswordChangeView(BasePasswordChangeView):
    """
    Password change view.

    This view allows users to change their password.

    Methods:
        None

    Attributes:
        form_class: The form class to use for password change.
    """
    form_class = PasswordChangeForm


class PasswordChangeDoneView(BasePasswordChangeDoneView):
    """
    Password change done view.

    This view is displayed after a successful password change.

    Methods:
        None

    Attributes:
        None
    """
    pass


class UserDetailView(DetailView):
    """
    User detail view.

    This view displays detailed information about a user.

    Methods:
        None

    Attributes:
        None
    """
    # TODO: Implement a public user profile page.
    pass


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    User list view.

    This view displays a list of users for administrators.

    Methods:
        get_queryset(self): Retrieves the list of users.

    Attributes:
        model: The User model.
        template_name: The name of the template to use for rendering the view.
        context_object_name: The name of the context variable containing user data.
        permission_required: The required permission to access the view.
    """
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'user_data'

    permission_required = 'users.view_user'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager').exists():
            queryset = queryset.all()
        else:
            raise Http404
        return queryset


def ban_user(request, *args, **kwargs):
    """
    Ban or unban a user.

    This view allows administrators to ban or unban a user.

    Args:
        request: The HTTP request object.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Redirects to the user list view.
    """
    if request.method == 'GET':
        user_pk = kwargs.get('pk')
        user = User.objects.filter(pk=user_pk).first()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()

    return redirect(reverse_lazy('users:users_list'))
