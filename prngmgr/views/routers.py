# Copyright 2016-2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Routers view module for prngmgr."""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseRedirect
)
from django.template import loader

from prngmgr import forms, models
from prngmgr.views import utils


@login_required
def routers(request, rtr_id):
    """Render routers view."""
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
                except Exception:
                    return HttpResponseNotFound(rtr_id)
                form = forms.PeeringRouterForm(request.POST, instance=router)
            router = form.save()
            return HttpResponseRedirect(reverse('prngmgr-routers',
                                                kwargs={'rtr_id': router.id}))
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
                except Exception:
                    return HttpResponseNotFound(rtr_id)
                key = router.hostname
                form = forms.PeeringRouterForm(instance=router)
                children = [
                    {'title': 'Peering Interfaces', 'forms': []}
                ]
                interfaces = models.PeeringRouterIXInterface.objects.filter(
                    prngrtr=router)
                for interface in interfaces:
                    children[0]['forms'].append({
                        'post': reverse('prngmgr-interfaces', kwargs={'if_id': interface.id, 'if_delete': '/delete'}),
                        'form': forms.PeeringRouterIXInterfaceForm(instance=interface),
                        'submit': {'class': 'btn btn-danger', 'value': 'Delete'},
                    })
                children[0]['forms'].append({
                    'post': reverse('prngmgr-interfaces', kwargs={'if_id': 0}),
                    'form': forms.NewPeeringRouterIXInterfaceForm(initial={'prngrtr': router.id}),
                    'submit': {'class': 'btn btn-primary', 'value': 'Add'},
                })
            context['form'] = {
                'parent': form,
                'children': children,
                'info': {
                    'title': 'Peering Router',
                    'key': key,
                    'post': reverse('prngmgr-routers', kwargs={'rtr_id': rtr_id}),
                },
            }
        else:
            # TODO: Add actions menu, selectable rows
            template = loader.get_template('prngmgr/table.html')
            table = {
                'name': 'routers',
                'title': 'Peering Routers',
                'cols': [
                    {'title': 'Hostname'},
                    {'title': 'Peering Interfaces'},
                    {'title': 'Possible Sessions'},
                    {'title': 'Provisioned Sessions'},
                    {'title': 'Established Sessions'},
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
                row = {'fields': []}
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
