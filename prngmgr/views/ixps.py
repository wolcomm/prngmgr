from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from django_peeringdb.models.concrete import Network, InternetExchange, NetworkIXLan
from prngmgr import settings, models

me = Network.objects.get(asn=settings.MY_ASN)


def ixps(request, ixp_id):
    template = loader.get_template('prngmgr/table.html')
    context = {
        'view': 'ixps',
        'table': {
            'name': 'ixps',
            'title': 'Internet Exchange Points',
            'cols': [
                { 'title': 'IXP Name' },
                { 'title': 'Country' },
                { 'title': 'Region' },
                { 'title': 'Participants' },
                { 'title': 'Possible Sessions' },
                { 'title': 'Provisioned Sessions' },
                { 'title': 'Established Sessions' },
            ],
            'rows': [
            ],
        },
    }
    ixps = InternetExchange.objects.all()
    for ixp in ixps:
        participants = NetworkIXLan.objects.filter(ixlan__ix=ixp).aggregate(count=Count('asn', distinct=True))
        sessions = models.PeeringSession.objects.filter(prngrtriface__netixlan__ixlan__ix=ixp)
        calculated = _render_alerts({
            'count': {
                'participants': participants['count'],
                'possible': sessions.count(),
                'provisioned': sessions.filter(provisioning_state=models.PeeringSession.PROV_COMPLETE).count(),
                'established': sessions.filter(operational_state=models.PeeringSession.OPER_ESTABLISHED).count(),
            },
        })
        row = { 'fields': [] }
        row['fields'].append({
            'display': ixp.name,
        })
        row['fields'].append({
            'display': ixp.country,
        })
        row['fields'].append({
            'display': ixp.region_continent,
        })
        row['fields'].append({
            'display': calculated['count']['participants'],
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
