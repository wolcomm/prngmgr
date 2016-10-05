from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseNotAllowed
from django.template import loader
from django_peeringdb.models.concrete import Network
from prngmgr import settings, forms, models
from prngmgr.views import utils

me = Network.objects.get(asn=settings.MY_ASN)


@login_required
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
                form = forms.PeeringRouterForm(request.POST)
            else:
                try:
                    router = models.PeeringRouter.objects.get(id=rtr_id)
                except:
                    return HttpResponseNotFound(rtr_id)
                form = forms.PeeringRouterForm(request.POST, instance=router)
            router = form.save()
            return HttpResponseRedirect(reverse('prngmgr-routers', kwargs = { 'rtr_id': router.id }))
        else:
            return HttpResponseRedirect(reverse('prngmgr-routers'))
    elif request.method == 'GET':
        if rtr_id:
            template = loader.get_template('prngmgr/form.html')
            if int(rtr_id) == 0:
                key = 'New'
                form = forms.PeeringRouterForm()
                children = []
            else:
                # TODO: Add "Delete" and "Back" controls
                try:
                    router = models.PeeringRouter.objects.get(id=rtr_id)
                except:
                    return HttpResponseNotFound(rtr_id)
                key = router.hostname
                form = forms.PeeringRouterForm(instance=router)
                children = [
                    { 'title': 'Peering Interfaces', 'forms': [] }
                ]
                interfaces = models.PeeringRouterIXInterface.objects.filter(prngrtr=router)
                for interface in interfaces:
                    children[0]['forms'].append({
                        'post': reverse('prngmgr-interfaces', kwargs = { 'if_id': interface.id, 'if_delete': '/delete' }),
                        'form': forms.PeeringRouterIXInterfaceForm(instance=interface),
                        'submit': {'class': 'btn btn-danger', 'value': 'Delete'},
                    })
                children[0]['forms'].append({
                    'post': reverse('prngmgr-interfaces', kwargs = { 'if_id': 0 }),
                    'form': forms.NewPeeringRouterIXInterfaceForm(initial={'prngrtr': router.id}),
                    'submit': {'class': 'btn btn-primary', 'value': 'Add'},
                })
            context['form'] = {
                'parent': form,
                'children': children,
                'info': {
                    'title': 'Peering Router',
                    'key': key,
                    'post': reverse('prngmgr-routers', kwargs = { 'rtr_id': rtr_id }),
                },
            }
        else:
            # TODO: Add actions menu, selectable rows
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
                'select': {
                    'style': 'single',
                    'blurable': 'true',
                },
            }
            routers = models.PeeringRouter.objects.all()
            for router in routers:
                interfaces = models.PeeringRouterIXInterface.objects.filter(prngrtr=router)
                sessions = models.PeeringSession.objects.filter(prngrtriface__prngrtr=router)
                calculated = utils.render_alerts({
                    'count': {
                        'interfaces': interfaces.count(),
                        'possible': sessions.count(),
                        'provisioned': sessions.filter(provisioning_state=models.PeeringSession.PROV_COMPLETE).count(),
                        'established': sessions.filter(operational_state=models.PeeringSession.OPER_ESTABLISHED).count(),
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
