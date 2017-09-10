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
"""Interfaces view module for prngmgr."""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseRedirect,
)

from prngmgr import forms, models


@login_required
def interfaces(request, if_id, if_delete):
    """Render interfaces view."""
    if request.method == 'POST':
        if if_id:
            if_id = int(if_id)
            if if_id == 0:
                form = forms.PeeringRouterIXInterfaceForm(request.POST)
            else:
                try:
                    interface = models.PeeringRouterIXInterface.objects.get(
                        id=if_id)
                except Exception:
                    return HttpResponseNotFound(if_id)
                if if_delete:
                    router = interface.prngrtr
                    models.PeeringRouterIXInterface.objects.filter(
                        id=if_id).delete()
                    return HttpResponseRedirect(reverse(
                        'prngmgr-routers', kwargs={'rtr_id': router.id}))
                form = forms.PeeringRouterIXInterfaceForm(request.POST,
                                                          instance=interface)
            interface = form.save()
            router = interface.prngrtr
            return HttpResponseRedirect(reverse('prngmgr-routers',
                                                kwargs={'rtr_id': router.id}))
        else:
            return HttpResponseRedirect(reverse('prngmgr-routers'))
    else:
        return HttpResponseNotAllowed(['POST'])
