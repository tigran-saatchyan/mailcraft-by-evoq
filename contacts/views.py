from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)

from contacts.forms import ContactForm, ListForm
from contacts.models import Contacts, Lists, ContactsList


def get_list_active_contacts(contact_list):
    contact_activity_status = {}
    total = len(contact_list)
    active = len(
        [
            contact
            for contact in contact_list
            if contact.contact.status.id == 1
        ]
    )
    inactive = total - active
    contact_activity_status['total'] = total
    contact_activity_status['active'] = active
    contact_activity_status['inactive'] = inactive
    return contact_activity_status


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
    success_url = reverse_lazy('contacts:list_contact')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lists = []
        for list_object in context['lists']:
            contact = []
            contact_list = ContactsList.objects.filter(list=list_object.pk)
            contact_activity_status = get_list_active_contacts(contact_list)
            contact.append(list_object)
            contact.append(contact_activity_status)
            lists.append(contact)
        context['lists'] = lists
        return context


class ListsDetailView(DetailView):
    model = Lists
    template_name = 'contacts/list/lists_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_of_contacts = ContactsList.objects.filter(
            list=self.kwargs.get('pk')
        )
        contact_activity_status = get_list_active_contacts(list_of_contacts)
        current_list = self.object

        context['contact_activity_status'] = contact_activity_status
        context['current_list'] = current_list

        context['lists'] = []
        for contact in list_of_contacts:
            contacts = []
            contact_in_lists = ContactsList.objects.filter(
                contact=contact.contact.pk
            )
            contacts.append(contact)
            contacts.append(contact_in_lists)
            context['lists'].append(contacts)

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
