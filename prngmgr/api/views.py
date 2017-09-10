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
"""Views module for prngmgr API."""

from django.db.models import F, Q

from django_peeringdb.models import concrete as pdb_models

from prngmgr import models as prngmgr_models
from prngmgr.api import datatables, serializers

from rest_framework import permissions, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """Organization view set."""

    queryset = pdb_models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """Facility view set."""

    queryset = pdb_models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkProxyViewSet(viewsets.ReadOnlyModelViewSet):
    """Network proxy view set."""

    queryset = prngmgr_models.NetworkProxy.objects.all()
    serializer_class = serializers.NetworkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def datatable(self, request, *args, **kwargs):
        """Render datatable query response."""
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
        """Render datatable table definition."""
        columns = [
            {'title': 'Network Name',
             'data': 'name',
             'name': 'name'},
            {'title': 'Primary ASN',
             'data': 'asn',
             'name': 'asn'},
            {'title': 'IRR Record',
             'data': 'irr_as_set',
             'name': 'irr_as_set'},
            {'title': 'Looking Glass',
             'data': 'looking_glass',
             'name': 'looking_glass'},
            {'title': 'Peering Policy',
             'data': 'policy_general',
             'name': 'policy_general'},
            {'title': 'Possible Sessions',
             'data': 'possible_sessions',
             'name': 'possible_sessions',
             'orderable': False,
             'searchable': False},
            {'title': 'Provisioned Sessions',
             'data': 'provisioned_sessions',
             'name': 'provisioned_sessions',
             'orderable': False,
             'searchable': False},
            {'title': 'Established Sessions',
             'data': 'established_sessions',
             'name': 'established_sessions',
             'orderable': False,
             'searchable': False},
        ]
        definition = datatables.TableDefView(columns=columns)
        return definition.response


class InternetExchangeProxyViewSet(viewsets.ReadOnlyModelViewSet):
    """IXP proxy view set."""

    queryset = prngmgr_models.InternetExchangeProxy.objects.all()
    serializer_class = serializers.InternetExchangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def datatable(self, request, *args, **kwargs):
        """Render datatable query response."""
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
        """Render datatable table definition."""
        columns = [
            {'title': 'IXP Name',
             'data': 'name',
             'name': 'name',
             'path': 'value'},
            {'title': 'Country',
             'data': 'country',
             'name': 'country'},
            {'title': 'Region',
             'data': 'region_continent',
             'name': 'region_continent'},
            {'title': 'Participants',
             'data': 'participants',
             'name': 'participants',
             'orderable': True,
             'searchable': False},
            {'title': 'Possible Sessions',
             'data': 'possible_sessions',
             'name': 'possible_sessions',
             'orderable': False,
             'searchable': False},
            {'title': 'Provisioned Sessions',
             'data': 'provisioned_sessions',
             'name': 'provisioned_sessions',
             'orderable': False,
             'searchable': False},
            {'title': 'Established Sessions',
             'data': 'established_sessions',
             'name': 'established_sessions',
             'orderable': False,
             'searchable': False},
        ]
        definition = datatables.TableDefView(columns=columns)
        return definition.response


class InternetExchangeFacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """IXP Facility proxy view set."""

    queryset = pdb_models.InternetExchangeFacility.objects.all()
    serializer_class = serializers.InternetExchangeFacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)


class IXLanViewSet(viewsets.ReadOnlyModelViewSet):
    """IXP LAN view set."""

    queryset = pdb_models.IXLan.objects.all()
    serializer_class = serializers.IXLanSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IXLanPrefixViewSet(viewsets.ReadOnlyModelViewSet):
    """IXP LAN prefix view set."""

    queryset = pdb_models.IXLanPrefix.objects.all()
    serializer_class = serializers.IXLanPrefixSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkContactViewSet(viewsets.ReadOnlyModelViewSet):
    """Network contact view set."""

    queryset = pdb_models.NetworkContact.objects.all()
    serializer_class = serializers.NetworkContactSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkFacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """Network facility view set."""

    queryset = pdb_models.NetworkFacility.objects.all()
    serializer_class = serializers.NetworkFacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkIXLanViewSet(viewsets.ReadOnlyModelViewSet):
    """Network IX LAN view set."""

    queryset = pdb_models.NetworkIXLan.objects.all()
    serializer_class = serializers.NetworkIXLanSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PeeringRouterViewSet(viewsets.ModelViewSet):
    """Peering router view set."""

    queryset = prngmgr_models.PeeringRouter.objects.all()
    serializer_class = serializers.PeeringRouterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def datatable(self, request, *args, **kwargs):
        """Render datatable query response."""
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
        """Render datatable table definition."""
        columns = [
            {'title': 'Hostname',
             'data': 'hostname',
             'name': 'hostname'},
            {'title': 'Peering Interfaces',
             'data': 'peering_interfaces',
             'name': 'peering_interfaces'},
            {'title': 'Possible Sessions',
             'data': 'possible_sessions',
             'name': 'possible_sessions',
             'orderable': False,
             'searchable': False},
            {'title': 'Provisioned Sessions',
             'data': 'provisioned_sessions',
             'name': 'provisioned_sessions',
             'orderable': False,
             'searchable': False},
            {'title': 'Established Sessions',
             'data': 'established_sessions',
             'name': 'established_sessions',
             'orderable': False,
             'searchable': False},
        ]
        definition = datatables.TableDefView(columns=columns)
        return definition.response


class PeeringRouterIXInterfaceViewSet(viewsets.ModelViewSet):
    """Peering router IX interface view set."""

    queryset = prngmgr_models.PeeringRouterIXInterface.objects.all()
    serializer_class = serializers.PeeringRouterIXInterfaceSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PeeringSessionViewSet(viewsets.ModelViewSet):
    """Peering session view set."""

    model_manager = prngmgr_models.PeeringSession.objects
    queryset = model_manager.all()
    serializer_class = serializers.PeeringSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def status_summary(self, *args, **kwargs):
        """Render status summary response."""
        summary = self.model_manager.status_summary()
        return Response(summary)

    @list_route()
    def state_changes(self, request, *args, **kwargs):
        """Render state changes query response."""
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params,
            static_exclude=Q(**{"session_state": F("previous_state")}),
            static_order='-state_changed',
        )
        return query.response

    @list_route()
    def datatable(self, request, *args, **kwargs):
        """Render datatable query response."""
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
        """Render datatable table definition."""
        columns = [
            {'title': 'IXP',
             'data': 'ixp_name',
             'name': 'ixp_name',
             'responsivePriority': 5},
            {'title': 'Peer Name',
             'data': 'remote_network_name',
             'name': 'remote_network_name',
             'responsivePriority': 1},
            {'title': 'Peer AS',
             'data': 'remote_network_asn',
             'name': 'remote_network_asn',
             'responsivePriority': 2},
            {'title': 'Address Family',
             'data': 'address_family',
             'name': 'address_family',
             'responsivePriority': 3},
            {'title': 'Peer Address',
             'data': 'remote_address',
             'name': 'remote_address'},
            {'title': 'Router',
             'data': 'router_hostname',
             'name': 'router_hostname'},
            {'title': 'State',
             'data': 'session_state',
             'name': 'session_state',
             'responsivePriority': 4},
            {'title': 'Accepted Prefixes',
             'data': 'accepted_prefixes',
             'name': 'accepted_prefixes',
             'responsivePriority': 6}
        ]
        definition = datatables.TableDefView(columns=columns)
        return definition.response
