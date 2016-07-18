from collections import Counter
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
    HttpResponseNotAllowed,
)
from django.template import loader
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory

from django_peeringdb.models.concrete import *

from ipaddress import *

from prngmgr.settings import *
from prngmgr.models import *
from prngmgr.forms import *
from prngmgr.snmp import Get, GetBGPTable

me = Network.objects.get(asn=MY_ASN)

def index(request):
    template = loader.get_template('prngmgr/index.html')
    context = {
        'me': me,
    }
    return HttpResponse(template.render(context, request))

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
        },
        'filter': {
        },
    }
    if filter_field:
        context['filter'] = {
            'field': filter_field,
            'arg': filter_arg,
        }
        sessions = PeeringSession.objects.filter(**{filter_field: filter_arg})
    else:
        sessions = PeeringSession.objects.all()
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
        'filter': {
        },
    }
    networks = Network.objects.all()
    for network in networks:
        sessions = PeeringSession.objects.filter(peer_netixlan__net=network)
        calculated = _render_alerts({
            'count': {
                'possible': sessions.count(),
                'provisioned': sessions.filter(provisioning_state=PeeringSession.PROV_COMPLETE).count(),
                'established': sessions.filter(operational_state=PeeringSession.OPER_ESTABLISHED).count(),
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

def routers(request, rtr_id):
    context = {
        'view': {
            'name': 'routers',
            'url': reverse('prngmgr-routers'),
        }
    }
    if request.method == 'POST':
        if rtr_id:
            template = loader.get_template('prngmgr/form.html')
            if int(rtr_id) == 0:
                form = PeeringRouterForm(request.POST)
            else:
                try:
                    router = PeeringRouter.objects.get(id=rtr_id)
                except:
                    return HttpResponseNotFound(rtr_id)
                form = PeeringRouterForm(request.POST, instance=router)
            router = form.save()
            return HttpResponseRedirect(reverse('prngmgr-routers', kwargs = { 'rtr_id': router.id }))
        else:
            return HttpResponseRedirect(reverse('prngmgr-routers'))
    elif request.method == 'GET':
        if rtr_id:
            template = loader.get_template('prngmgr/form.html')
            if int(rtr_id) == 0:
                key = 'New'
                form = PeeringRouterForm()
            else:
                try:
                    router = PeeringRouter.objects.get(id=rtr_id)
                except:
                    return HttpResponseNotFound(rtr_id)
                key = router.hostname
                form = PeeringRouterForm(instance=router)
                InterfaceFormSet = inlineformset_factory(
                    PeeringRouter, PeeringRouterIXInterface,
                    form=PeeringRouterIXInterfaceForm,
                    fields=('netixlan',),
                    labels={ 'netixlan': "IX LAN Interface"},
                    extra=2
                )
                formset = InterfaceFormSet(instance=router)
            context['form'] = {
                'parent': form,
                'children': [
                    { 'title': 'Peering Interfaces', 'formset': formset },
                ],
                'info': {
                    'title': 'Peering Router',
                    'key': key,
                    'post': reverse('prngmgr-routers', kwargs = { 'rtr_id': rtr_id }),
                },
            }
        else:
            template = loader.get_template('prngmgr/table.html')
            table = {
                'name': 'routers',
                'title': 'Peering Routers',
                'cols': [
                    { 'title': 'Hostname' },
                    { 'title': 'Peering Interfaces' },
                    { 'title': 'Possible Sessions' },
                    { 'title': 'Provisioned Sessions' },
                    { 'title': 'Established Sessions' },
                ],
                'rows': [
                ],
                'filter': {
                },
            }
            routers = PeeringRouter.objects.all()
            for router in routers:
                interfaces = PeeringRouterIXInterface.objects.filter(prngrtr=router)
                sessions = PeeringSession.objects.filter(prngrtriface__prngrtr=router)
                calculated = _render_alerts({
                    'count': {
                        'interfaces': interfaces.count(),
                        'possible': sessions.count(),
                        'provisioned': sessions.filter(provisioning_state=PeeringSession.PROV_COMPLETE).count(),
                        'established': sessions.filter(operational_state=PeeringSession.OPER_ESTABLISHED).count(),
                    },
                })
                row = { 'fields': [] }
                row['fields'].append({
                    'display': router.hostname,
                    'link': reverse('prngmgr-routers', kwargs={'rtr_id': router.id}),
                })
                row['fields'].append({
                    'display': calculated['count']['interfaces'],
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
                table['rows'].append(row)
            context['table'] = table
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

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
        'filter': {
        },
    }
    ixps = InternetExchange.objects.all()
    for ixp in ixps:
        participants = NetworkIXLan.objects.filter(ixlan__ix=ixp).aggregate(count=Count('asn', distinct=True))
        sessions = PeeringSession.objects.filter(prngrtriface__netixlan__ixlan__ix=ixp)
        calculated = _render_alerts({
            'count': {
                'participants': participants['count'],
                'possible': sessions.count(),
                'provisioned': sessions.filter(provisioning_state=PeeringSession.PROV_COMPLETE).count(),
                'established': sessions.filter(operational_state=PeeringSession.OPER_ESTABLISHED).count(),
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
            'possible': ALERT_NONE,
            'provisioned': ALERT_NONE,
            'established': ALERT_NONE,
        }
    else:
        if calculated['count']['provisioned'] == 0:
            calculated['alert'] = {
                'possible': ALERT_SUCCESS,
                'provisioned': ALERT_DANGER,
                'established': ALERT_DANGER,
            }
        elif calculated['count']['provisioned'] < calculated['count']['possible']:
            if calculated['count']['established'] < calculated['count']['provisioned']:
                calculated['alert'] = {
                    'possible': ALERT_SUCCESS,
                    'provisioned': ALERT_WARNING,
                    'established': ALERT_DANGER,
                }
            else:
                calculated['alert'] = {
                    'possible': ALERT_SUCCESS,
                    'provisioned': ALERT_WARNING,
                    'established': ALERT_WARNING,
                }
        else:
            if calculated['count']['established'] < calculated['count']['provisioned']:
                calculated['alert'] = {
                    'possible': ALERT_SUCCESS,
                    'provisioned': ALERT_SUCCESS,
                    'established': ALERT_DANGER,
                }
            else:
                calculated['alert'] = {
                    'possible': ALERT_SUCCESS,
                    'provisioned': ALERT_SUCCESS,
                    'established': ALERT_SUCCESS,
                }
    return calculated

