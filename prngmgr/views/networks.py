from django.http import HttpResponse
from django.template import loader
from django_peeringdb.models.concrete import Network
from prngmgr import settings, models

me = Network.objects.get(asn=settings.MY_ASN)


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
        calculated = _render_alerts({
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


def _render_alerts(calculated):
    if calculated['count']['possible'] == 0:
        calculated['alert'] = {
            'possible': models.ALERT_NONE,
            'provisioned': models.ALERT_NONE,
            'established': models.ALERT_NONE,
        }
    else:
        if calculated['count']['provisioned'] == 0:
            calculated['alert'] = {
                'possible': models.ALERT_SUCCESS,
                'provisioned': models.ALERT_DANGER,
                'established': models.ALERT_DANGER,
            }
        elif calculated['count']['provisioned'] < calculated['count']['possible']:
            if calculated['count']['established'] < calculated['count']['provisioned']:
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_WARNING,
                    'established': models.ALERT_DANGER,
                }
            else:
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_WARNING,
                    'established': models.ALERT_WARNING,
                }
        else:
            if calculated['count']['established'] < calculated['count']['provisioned']:
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_SUCCESS,
                    'established': models.ALERT_DANGER,
                }
            else:
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_SUCCESS,
                    'established': models.ALERT_SUCCESS,
                }
    return calculated
