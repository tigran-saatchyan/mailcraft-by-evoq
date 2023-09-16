from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)

from contacts.forms import ContactForm, ListForm
from contacts.models import Contacts, Lists, ContactsList


def get_list_active_contacts(contact_list):
    """
    Get the count of active and inactive contacts in a list.

    Args:
        contact_list (QuerySet): The queryset of ContactsList objects.

    Returns:
        dict: A dictionary containing counts of total, active, and inactive contacts.
    """
    contact_activity_status = {}
    total = len(contact_list)
    active = len(
        [
            contact
            for contact in contact_list
            if contact.contact.status == 'active'
        ]
    )
    inactive = total - active
    contact_activity_status['total'] = total
    contact_activity_status['active'] = active
    contact_activity_status['inactive'] = inactive
    return contact_activity_status


class ContactCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new contact.

    Attributes:
        model (Contacts): The model associated with this view.
        template_name (str): The name of the template to render.
        form_class (ContactForm): The form class to use for creating a new contact.
        success_url (str): The URL to redirect to after successful contact creation.

    Methods:
        form_valid: Override to assign the user to the contact before saving.
        get_queryset: Filter contacts based on user authentication.
    """
    model = Contacts
    template_name = 'contacts/contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:create_contact')

    def form_valid(self, form):
        """
        Override to assign the user to the contact before saving.

        Args:
            form (ContactForm): The form object containing contact data.

        Returns:
            HttpResponse: The response after successfully saving the form.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        """
        Filter contacts based on user authentication.

        Returns:
            queryset: The filtered queryset of contacts.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(
            user=self.request.user,
            list__user=self.request.user
        )
        return queryset


class ContactListView(LoginRequiredMixin, ListView):
    """
    View for listing contacts.

    Attributes:
        model (Contacts): The model associated with this view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the variable to use in the template for the list of contacts.

    Methods:
        get_queryset: Filter contacts based on user authentication.
    """
    model = Contacts
    template_name = 'contacts/contact/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        """
        Filter contacts based on user authentication.

        Returns:
            queryset: The filtered queryset of contacts.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ContactDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying a single contact.

    Attributes:
        model (Contacts): The model associated with this view.
        template_name (str): The name of the template to render.

    """
    model = Contacts
    template_name = 'contacts/contact/contact_detail.html'


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing contact.

    Attributes:
        model (Contacts): The model associated with this view.
        form_class (ContactForm): The form class to use for updating the contact.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after successful contact update.

    Methods:
        get_queryset: Filter contacts based on user authentication.
    """
    model = Contacts
    form_class = ContactForm
    template_name = 'contacts/contact/contact_form.html'
    success_url = reverse_lazy('contacts:list_contact')

    def get_queryset(self):
        """
        Filter contacts based on user authentication.

        Returns:
            queryset: The filtered queryset of contacts.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a contact.

    Attributes:
        model (Contacts): The model associated with this view.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after successful contact deletion.

    """
    model = Contacts
    template_name = 'contacts/contact/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts:list_contact')


# *********************************************************
# TODO: Add checks for list ownership by the user
class ListsCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new contact list.

    Attributes:
        model (Lists): The model associated with this view.
        template_name (str): The name of the template to render.
        form_class (ListForm): The form class to use for creating a new list.
        success_url (str): The URL to redirect to after successful list creation.

    Methods:
        form_valid: Override to assign the user to the list before saving.
    """
    model = Lists
    template_name = 'contacts/list/lists_form.html'
    form_class = ListForm
    success_url = reverse_lazy('contacts:create_list')

    def form_valid(self, form):
        """
        Override to assign the user to the list before saving.

        Args:
            form (ListForm): The form object containing list data.

        Returns:
            HttpResponse: The response after successfully saving the form.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ListsListView(LoginRequiredMixin, ListView):
    """
    View for listing contact lists.

    Attributes:
        model (Lists): The model associated with this view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the variable to use in the template for the list of lists.

    Methods:
        get_queryset: Filter lists based on user authentication.
        get_context_data: Add additional context data for the template.
    """
    model = Lists
    template_name = 'contacts/list/lists_list.html'
    context_object_name = 'lists'
    success_url = reverse_lazy('contacts:list_list')

    def get_queryset(self):
        """
        Filter lists based on user authentication.

        Returns:
            queryset: The filtered queryset of lists.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The updated context data.
        """
        context = super().get_context_data(**kwargs)

        lists = []
        for list_object in context['lists']:
            contact = []
            contact_list = ContactsList.objects.filter(
                list=list_object.pk
            )
            contact_activity_status = get_list_active_contacts(contact_list)
            contact.append(list_object)
            contact.append(contact_activity_status)
            lists.append(contact)
        context['lists'] = lists
        return context


class ListsDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying details of a contact list.

    Attributes:
        model (Lists): The model associated with this view.
        template_name (str): The name of the template to render.

    Methods:
        get_context_data: Add additional context data for the template.
    """
    model = Lists
    template_name = 'contacts/list/lists_detail.html'

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The updated context data.
        """
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
                contact=contact.contact.pk,
                list__user=self.request.user
            )
            contacts.append(contact)
            contacts.append(contact_in_lists)
            context['lists'].append(contacts)

        return context


class ListsUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing contact list.

    Attributes:
        model (Lists): The model associated with this view.
        form_class (ListForm): The form class to use for updating the list.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after successful list update.

    Methods:
        get_queryset: Filter lists based on user authentication.
        form_valid: Override to assign the user to the list before saving.
    """
    model = Lists
    form_class = ListForm
    template_name = 'contacts/list/lists_form.html'
    success_url = reverse_lazy('contacts:list_list')

    def get_queryset(self):
        """
        Filter lists based on user authentication.

        Returns:
            queryset: The filtered queryset of lists.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        """
        Override to assign the user to the list before saving.

        Args:
            form (ListForm): The form object containing list data.

        Returns:
            HttpResponse: The response after successfully saving the form.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ListsDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a contact list.

    Attributes:
        model (Lists): The model associated with this view.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after successful list deletion.

    """
    model = Lists
    template_name = 'contacts/list/lists_confirm_delete.html'
    success_url = reverse_lazy('contacts:list_list')
