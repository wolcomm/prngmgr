from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django_peeringdb.models.concrete import Network
from prngmgr import settings
from prngmgr.models import models
from prngmgr.views import utils

me = Network.objects.get(asn=settings.MY_ASN)


class IndexView(TemplateView):
    template_name = 'prngmgr/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return {'me': me}


class NetworksView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    def get_context_data(self, **kwargs):
        context = super(NetworksView, self).get_context_data(**kwargs)
        context['columns'] = reverse_lazy('network-tabledef')
        context['api'] = reverse_lazy('network-datatable')
        context['table'] = {
            'name': 'networks',
            'title': 'Peering Networks',
        }
        return context


class InternetExchangeView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    def get_context_data(self, **kwargs):
        context = super(InternetExchangeView, self).get_context_data(**kwargs)
        context['columns'] = reverse_lazy('internetexchange-tabledef')
        context['api'] = reverse_lazy('internetexchange-datatable')
        context['table'] = {
            'name': 'ixps',
            'title': 'Internet Exchange Points',
        }
        return context


class PeeringSessionsView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    def get_context_data(self, **kwargs):
        context = super(PeeringSessionsView, self).get_context_data(**kwargs)
        context['columns'] = reverse_lazy('peeringsession-tabledef')
        context['api'] = reverse_lazy('peeringsession-datatable')
        context['table'] = {
            'name': 'sessions',
            'title': 'Peering Sessions',
        }
        return context
