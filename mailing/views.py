from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from mailing.forms import MailingForm, MailingSettingsForm
from mailing.models import Mailing, MailingSettings
from mailing.service import create_cron_jobs, remove_cron_jobs


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new mailing.

    Args:
        LoginRequiredMixin (class): A mixin to require user login.

    Attributes:
        model (class): The model used for the view.
        form_class (class): The form class used for creating the mailing.
        template_name (str): The name of the template for the view.
        success_url (str): The URL to redirect to upon successful creation.
        permission_required (str): The permission required to access this view.

    Methods:
        get_context_data: Get the context data for the view.
        form_valid: Handle form submission when valid.
    """
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:list_mailing')
    permission_required = 'mailing.add_mailing'

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        Returns:
            dict: A dictionary containing context data.
        """
        context = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(
            Mailing,
            MailingSettings,
            form=MailingSettingsForm,
            extra=1,
            can_delete=False
        )
        if self.request.method == 'POST':
            mailing_formset = MailingFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            mailing_formset = MailingFormset(instance=self.object)

        context['mailing_formset'] = mailing_formset

        return context

    def form_valid(self, form):
        """
        Handle form submission when valid.

        Args:
            form (Form): The form instance.

        Returns:
            HttpResponse: The HTTP response after successful form submission.
        """
        context_data = self.get_context_data()
        form.instance.user = self.request.user
        mailing_formset = context_data['mailing_formset']

        self.object = form.save(commit=False)
        self.object.save()

        mailing_formset.instance = self.object
        mailing_data = mailing_formset.save(commit=False)

        if mailing_data:
            mailing_settings_data = mailing_data[0]
        else:
            mailing_settings_data = MailingSettings()

        mailing_settings, created = MailingSettings.objects.get_or_create(
            mailing=self.object,
            defaults={
                'mailing_periods': mailing_settings_data.mailing_periods,
                'status': mailing_settings_data.status,
                'start_date': mailing_settings_data.start_date,
                'mailing_time': mailing_settings_data.mailing_time,
                'mailing_week_day_num': mailing_settings_data.mailing_week_day_num,
                'end_date': mailing_settings_data.end_date,
                'cron_setting': mailing_settings_data.cron_setting,
            }
        )
        self.object.setting = mailing_settings
        mailing_settings.save()

        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    """
    View for listing mailings.

    Args:
        LoginRequiredMixin (class): A mixin to require user login.

    Attributes:
        model (class): The model used for the view.
        template_name (str): The name of the template for the view.
        context_object_name (str): The name of the context object.

    Methods:
        get_queryset: Get the queryset for the view.
    """
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        """
        Get the queryset for the view.

        Returns:
            Queryset: The filtered queryset based on user and permissions.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager').exists():
            queryset = queryset.all()
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying mailing details.

    Args:
        LoginRequiredMixin (class): A mixin to require user login.

    Attributes:
        model (class): The model used for the view.
        template_name (str): The name of the template for the view.
        success_url (str): The URL to redirect to upon success.
        permission_required (str): The permission required to access this view.

    Methods:
        get_queryset: Get the queryset for the view.
    """
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    success_url = reverse_lazy('mailings:detail_mailing')
    permission_required = 'mailing.view_mailing'

    def get_queryset(self):
        """
        Get the queryset for the view.

        Returns:
            Queryset: The filtered queryset based on user and permissions.
        """
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager').exists():
            queryset = queryset.filter(
                id=self.kwargs.get('pk'),
            )
        else:
            queryset = queryset.filter(
                id=self.kwargs.get('pk'),
                user=self.request.user
            )

        return queryset


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating mailing details.

    Args:
        LoginRequiredMixin (class): A mixin to require user login.

    Attributes:
        model (class): The model used for the view.
        template_name (str): The name of the template for the view.
        form_class (class): The form class used for updating the mailing.
        success_url (str): The URL to redirect to upon success.

    Methods:
        get_context_data: Get the context data for the view.
        form_valid: Handle form submission when valid.
    """
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:list_mailing')

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        Returns:
            dict: A dictionary containing context data.
        """
        if self.request.user.groups.filter(name='manager').exists():
            raise Http404
        context = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(
            Mailing,
            MailingSettings,
            form=MailingSettingsForm,
            extra=1,
            can_delete=False
        )
        if self.request.method == 'POST':
            mailing_formset = MailingFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            mailing_formset = MailingFormset(instance=self.object)

        context['mailing_formset'] = mailing_formset

        return context

    def form_valid(self, form):
        """
        Handle form submission when valid.

        Args:
            form (Form): The form instance.

        Returns:
            HttpResponse: The HTTP response after successful form submission.
        """
        context_data = self.get_context_data()
        mailing_formset = context_data['mailing_formset']

        self.object = form.save(commit=False)
        if mailing_formset.is_valid():
            mailing_formset.instance = self.object
            mailing_formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a mailing.

    Args:
        LoginRequiredMixin (class): A mixin to require user login.

    Attributes:
        model (class): The model used for the view.
        template_name (str): The name of the template for the view.
        success_url (str): The URL to redirect to upon success.

    Methods:
        get_context_data: Get the context data for the view.
    """
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:list_mailing')

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        Returns:
            dict: A dictionary containing context data.
        """
        if self.request.user.groups.filter(name='manager').exists():
            raise Http404
        context = super().get_context_data(**kwargs)
        return context


def start_stop_mailing(request, *args, **kwargs):
    """
    View for starting or stopping a mailing.

    Args:
        request (HttpRequest): The HTTP request object.
        *args: Variable length argument list.
        **kwargs: Keyword arguments.

    Returns:
        HttpResponse: The HTTP response after starting or stopping the mailing.
    """
    # TODO: Implement mailing start/stop logic here
    mailing_pk = kwargs.pop('pk')
    try:
        mailing = Mailing.objects.get(pk=mailing_pk)
    except Mailing.DoesNotExist:
        pass

    if mailing.setting.status == 'completed':
        if mailing.setting.start_date <= date.today() <= mailing.setting.end_date:
            mailing.setting.status = 'running'
            create_cron_jobs(mailing)
        else:
            print('mailing out of date')
    elif mailing.setting.status == 'running':
        mailing.setting.status = 'completed'
        remove_cron_jobs(mailing)
    mailing.setting.save()

    return redirect('mailings:list_mailing')
