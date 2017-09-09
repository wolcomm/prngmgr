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
"""Class based views module for prngmgr."""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_peeringdb.models.concrete import Network

from prngmgr import settings

def me():
    return Network.objects.get(asn=settings.MY_ASN)


class IndexView(TemplateView):
    template_name = 'prngmgr/index.html'

    @method_decorator(login_required(login_url='/auth/login/'))
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['me'] = me()
        return context


class NetworksView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NetworksView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NetworksView, self).get_context_data(**kwargs)
        context['table'] = {
            'name': 'networks',
            'title': 'Peering Networks',
            'api': {
                'definition': reverse_lazy('networkproxy-tabledef'),
                'data': reverse_lazy('networkproxy-datatable')
            }
        }
        return context


class InternetExchangeView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InternetExchangeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InternetExchangeView, self).get_context_data(**kwargs)
        context['table'] = {
            'name': 'ixps',
            'title': 'Internet Exchange Points',
            'api': {
                'definition': reverse_lazy('internetexchangeproxy-tabledef'),
                'data': reverse_lazy('internetexchangeproxy-datatable')
            }
        }
        return context


class PeeringSessionsView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeeringSessionsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PeeringSessionsView, self).get_context_data(**kwargs)
        context['table'] = {
            'name': 'sessions',
            'title': 'Peering Sessions',
            'api': {
                'definition': reverse_lazy('peeringsession-tabledef'),
                'data': reverse_lazy('peeringsession-datatable')
            }
        }
        return context


class PeeringRoutersView(TemplateView):
    template_name = 'prngmgr/ajax_table.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeeringRoutersView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PeeringRoutersView, self).get_context_data(**kwargs)
        context['table'] = {
            'name': 'routers',
            'title': 'Peering Routers',
            'api': {
                'definition': reverse_lazy('peeringrouter-tabledef'),
                'data': reverse_lazy('peeringrouter-datatable')
            }
        }
        return context
