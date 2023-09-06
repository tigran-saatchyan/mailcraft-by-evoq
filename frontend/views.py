from django.views.generic import ListView

from mailing.models import Mailing


# Create your views here.


class IndexPageView(ListView):
    model = Mailing
    template_name = 'frontend/index.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=3)
        return queryset
