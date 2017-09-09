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
"""URLconf module for prngmgr API."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from prngmgr.api import views


router = DefaultRouter()
router.register(r'org', views.OrganizationViewSet)
router.register(r'fac', views.FacilityViewSet)
router.register(r'net', views.NetworkProxyViewSet)
router.register(r'ix', views.InternetExchangeProxyViewSet)
router.register(r'ixfac', views.InternetExchangeFacilityViewSet)
router.register(r'ixlan', views.IXLanViewSet)
router.register(r'ixpfx', views.IXLanPrefixViewSet)
router.register(r'poc', views.NetworkContactViewSet)
router.register(r'netixlan', views.NetworkIXLanViewSet)
router.register(r'router', views.PeeringRouterViewSet)
router.register(r'interface', views.PeeringRouterIXInterfaceViewSet)
router.register(r'session', views.PeeringSessionViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
