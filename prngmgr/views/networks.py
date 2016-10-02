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


class NetworksView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'
    view = 'net'
    api = reverse_lazy('network-datatable')
    table = {
        'name': 'networks',
        'title': 'Peering Networks',
        'cols': [
            {'title': 'Network Name'},
            {'title': 'Primary ASN'},
            {'title': 'IRR Record'},
            {'title': 'Looking Glass'},
            {'title': 'Peering Policy'},
            {'title': 'Possible Sessions'},
            {'title': 'Provisioned Sessions'},
            {'title': 'Established Sessions'},
        ],
    }

    def get_context_data(self, **kwargs):
        context = super(NetworksView, self).get_context_data(**kwargs)
        context['view'] = self.view
        context['api'] = self.api
        context['table'] = self.table
        return context


@login_required
def networks(request, net_id):
    template = loader.get_template('prngmgr/table.html')
    context = {
        'view': 'networks',
        'table': {
            'name': 'networks',
            'title': 'Peering Networks',
            'cols': [
                { 'title': 'Network Name' },
                { 'title': 'Primary ASN' },
                { 'title': 'IRR Record' },
                { 'title': 'Looking Glass' },
                { 'title': 'Peering Policy' },
                { 'title': 'Possible Sessions' },
                { 'title': 'Provisioned Sessions' },
                { 'title': 'Established Sessions' },
            ],
            'rows': [
            ],
        },
    }
    networks = Network.objects.all()
    for network in networks:
        sessions = models.PeeringSession.objects.filter(peer_netixlan__net=network)
        calculated = utils.render_alerts({
            'count': {
                'possible': sessions.count(),
                'provisioned': sessions.filter(provisioning_state=models.PeeringSession.PROV_COMPLETE).count(),
                'established': sessions.filter(operational_state=models.PeeringSession.OPER_ESTABLISHED).count(),
            },
        })
        row = { 'fields': [] }
        row['fields'].append({
            'display': network.name,
        })
        row['fields'].append({
            'display': network.asn,
        })
        row['fields'].append({
            'display': network.irr_as_set,
        })
        row['fields'].append({
            'display': network.looking_glass,
            'link': network.looking_glass,
        })
        row['fields'].append({
            'display': network.policy_general,
        })
        row['fields'].append({
            'display': calculated['count']['possible'],
            'alert': calculated['alert']['possible'],
        })
        row['fields'].append({
            'display': calculated['count']['provisioned'],
            'alert': calculated['alert']['provisioned'],
        })
        row['fields'].append({
            'display': calculated['count']['established'],
            'alert': calculated['alert']['established'],
        })
        context['table']['rows'].append(row)
    return HttpResponse(template.render(context, request))
