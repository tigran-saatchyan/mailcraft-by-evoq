from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from mailing.forms import MailingForm
from mailing.models import Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:list_mailing')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset



class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    success_url = reverse_lazy('mailings:detail_mailing')


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:list_mailing')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:list_mailing')
