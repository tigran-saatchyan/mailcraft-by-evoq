from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from logs.models import Logging


class LoggingListView(ListView):
    """
    View for displaying a list of logging entries.

    This view displays a list of logging entries related to mailings.

    Attributes:
        model (Logging): The model associated with this view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the variable to use in the template for the list of logs.

    Methods:
        get_queryset: Override to filter logs based on the user's related mailings.

    """
    model = Logging
    template_name = 'logs/logs_detail.html'
    context_object_name = 'logs'

    def get_queryset(self):
        """
        Override to filter logs based on the user's related mailings.

        Returns:
            queryset: The filtered queryset of logs.

        """
        queryset = super().get_queryset()
        queryset.filter(mailing__user=self.request.user)
        return queryset


class LoggingDeleteView(DeleteView):
    """
    View for confirming the deletion of a logging entry.

    This view allows the user to confirm the deletion of a logging entry.

    Attributes:
        model (Logging): The model associated with this view.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after successful deletion.

    """
    model = Logging
    template_name = 'logs/logs_confirm_delete.html'
    success_url = reverse_lazy('logs:logs_list')
