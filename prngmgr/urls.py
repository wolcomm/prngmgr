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
"""URLconf module for prngmgr."""

from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from prngmgr import classy_views
from prngmgr.views import routers, interfaces

auth_urls = [
    url(r'^login/$', login, {'template_name': 'prngmgr/login.html'}, name="prngmgr-login"),
    url(r'^logout/$', logout,{'next_page': '/'}, name="prngmgr-logout"),
]

urlpatterns = [
    url(r'^$', classy_views.IndexView.as_view(), name="prngmgr-index"),
    url(r'^sessions/(?P<pk>\d+)?$', classy_views.PeeringSessionsView.as_view(), name="prngmgr-sessions"),
    url(r'^networks/(?P<pk>\d+)?$', classy_views.NetworksView.as_view(), name="prngmgr-networks"),
    url(r'^ixps/(?P<pk>\d+)?$', classy_views.InternetExchangeView.as_view(), name="prngmgr-ixps"),
    url(r'^crouters/(?P<pk>\d+)?$', classy_views.PeeringRoutersView.as_view(), name="prngmgr-crouters"),
    url(r'^routers/(?P<rtr_id>\d+)?$', routers.routers, name="prngmgr-routers"),
    url(r'^interfaces/(?P<if_id>\d+)?(?P<if_delete>/delete)?$', interfaces.interfaces, name="prngmgr-interfaces"),
    url(r'^auth/', include(auth_urls)),
    url(r'^api/', include('prngmgr.api.urls'))
]
