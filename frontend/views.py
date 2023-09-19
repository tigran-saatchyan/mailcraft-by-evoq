import random
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from blog.models import Posts
from contacts.models import ContactsList
from contacts.views import get_list_active_contacts
from mailing.models import Mailing

class IndexPageView(LoginRequiredMixin, ListView):
    """
    View for displaying the index page.

    This view displays the index page, which provides information about mailings, contact list activity, and recent blog posts.

    Attributes:
        model (Mailing): The model associated with this view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the variable to use in the template for the list of mailings.

    Methods:
        get_context_data: Override to provide additional context data for the template.
        get_queryset: Override to filter mailings based on user authentication and status.

    """
    model = Mailing
    template_name = 'frontend/index.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        """
        Override to provide additional context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The updated context data.

        """
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='manager').exists():
            context['total_mailings'] = Mailing.objects.filter(
            ).count()
            context['total_active_mailings'] = Mailing.objects.filter(
                setting__status='running'
            ).count()
        else:
            context['total_mailings'] = Mailing.objects.filter(
                user=self.request.user
            ).count()
            context['total_active_mailings'] = Mailing.objects.filter(
                user=self.request.user,
                setting__status='running'
            ).count()

        context['total_inactive_mailings'] = context['total_mailings'] - \
                                             context['total_active_mailings']

        list_of_contacts = ContactsList.objects.filter(
            list=self.kwargs.get('pk')
        )
        contact_activity_status = get_list_active_contacts(list_of_contacts)

        context['contact_activity_status'] = contact_activity_status

        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)
        random.seed(int(current_date.timestamp() * 1000))

        last_month_posts = list(
            Posts.objects.filter(
                creation_date__gte=thirty_days_ago,
                is_published=True
            ).all()
        )
        try:
            random_three_posts = random.sample(last_month_posts, 3)
            context['random_three_posts'] = random_three_posts
        except Exception:
            pass
        return context

    def get_queryset(self):
        """
        Override to filter mailings based on user authentication and status.

        Returns:
            queryset: The filtered queryset of mailings.

        """
        queryset = super().get_queryset().filter(
            user=self.request.user,
            setting__status='running'
        )
        return queryset
