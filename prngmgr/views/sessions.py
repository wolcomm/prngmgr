from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse
from django_peeringdb.models.concrete import Network
from prngmgr import settings, models

me = Network.objects.get(asn=settings.MY_ASN)


def sessions(request, filter_field, filter_arg):
    template = loader.get_template('prngmgr/table.html')
    context = {
        'view': 'sessions',
        'url_name': 'prngmgr-sessions',
        'table': {
            'name': 'sessions',
            'title': 'Peering Sessions',
            'cols': [
                { 'title': 'IXP' },
                { 'title': 'Router' },
                { 'title': 'Peer Name' },
                { 'title': 'Peer AS' },
                { 'title': 'Address Family' },
                { 'title': 'Peer Address' },
                { 'title': 'Provisioning State' },
                { 'title': 'Admin State' },
                { 'title': 'Operational State' },
            ],
            'rows': [
            ],
            'select': {
                'style': 'os',
                'blurable': 'true',
            },
        },
    }
    if filter_field:
        context['table']['filter'] = {
            'field': filter_field,
            'arg': filter_arg,
        }
        sessions = models.PeeringSession.objects.filter(**{filter_field: filter_arg})
    else:
        sessions = models.PeeringSession.objects.all()
    for session in sessions:
        row = { 'fields': [] }
        row['fields'].append({
            'display': session.prngrtriface.netixlan.ixlan.ix.name,
            'link': reverse('prngmgr-ixps', kwargs = { 'ixp_id': session.prngrtriface.netixlan.ixlan.ix.id })
        })
        row['fields'].append({
            'display': session.prngrtriface.prngrtr.hostname,
            'link': reverse('prngmgr-routers', kwargs = { 'rtr_id': session.prngrtriface.prngrtr.id })
        })
        row['fields'].append({
            'display': session.peer_netixlan.net.name,
            'link': reverse('prngmgr-networks', kwargs = { 'net_id': session.peer_netixlan.net.id })
        })
        row['fields'].append({
            'display': session.peer_netixlan.asn,
        })
        row['fields'].append({
            'display': session.get_af_display,
        })
        row['fields'].append({
            'display': session.get_remote_address,
        })
        row['fields'].append({
            'display': session.get_provisioning_state_display,
            'alert': session.get_provisioning_state_alert,
        })
        row['fields'].append({
            'display': session.get_admin_state_display,
            'alert': session.get_admin_state_alert,
        })
        row['fields'].append({
            'display': session.get_operational_state_display,
            'alert': session.get_operational_state_alert,
        })
        context['table']['rows'].append(row)
    return HttpResponse(template.render(context, request))
