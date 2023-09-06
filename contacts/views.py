from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)

from contacts.forms import ContactForm, ListForm
from contacts.models import Contacts, Lists, ContactsList


class ContactCreateView(CreateView):
    model = Contacts
    template_name = 'contacts/contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:create_contact')


class ContactListView(ListView):
    model = Contacts
    template_name = 'contacts/contact/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ContactDetailView(DetailView):
    model = Contacts
    template_name = 'contacts/contact/contact_detail.html'


class ContactUpdateView(UpdateView):
    model = Contacts
    form_class = ContactForm
    template_name = 'contacts/contact/contact_form.html'
    success_url = reverse_lazy('contacts:update_contact')


class ContactDeleteView(DeleteView):
    model = Contacts
    template_name = 'contacts/contact/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts:list_contact')


# *********************************************************

class ListsCreateView(CreateView):
    model = Lists
    template_name = 'contacts/list/lists_form.html'
    form_class = ListForm
    success_url = reverse_lazy('contacts:create_list')


class ListsListView(ListView):
    model = Lists
    template_name = 'contacts/list/lists_list.html'
    context_object_name = 'lists'
    success_url = reverse_lazy('contacts:list_list')


class ListsDetailView(DetailView):
    model = Lists
    template_name = 'contacts/list/lists_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_list = ContactsList.objects.filter(list=self.kwargs.get('pk'))
        context['contact_list'] = contact_list
        return context


class ListsUpdateView(UpdateView):
    model = Lists
    form_class = ListForm
    template_name = 'contacts/list/lists_form.html'
    success_url = reverse_lazy('contacts:list_list')


class ListsDeleteView(DeleteView):
    model = Lists
    template_name = 'contacts/list/lists_confirm_delete.html'
    success_url = reverse_lazy('contacts:list_list')
