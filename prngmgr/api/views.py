from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import list_route
from django_peeringdb.models import concrete as pdb_models
from prngmgr import models as prngmgr_models
from prngmgr.api import serializers, datatables


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkProxyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = prngmgr_models.NetworkProxy.objects.all()
    serializer_class = serializers.NetworkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def datatable(self, request, *args, **kwargs):
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
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
    queryset = prngmgr_models.InternetExchangeProxy.objects.all()
    serializer_class = serializers.InternetExchangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def datatable(self, request, *args, **kwargs):
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
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
    queryset = pdb_models.InternetExchangeFacility.objects.all()
    serializer_class = serializers.InternetExchangeFacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)


class IXLanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.IXLan.objects.all()
    serializer_class = serializers.IXLanSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IXLanPrefixViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.IXLanPrefix.objects.all()
    serializer_class = serializers.IXLanPrefixSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.NetworkContact.objects.all()
    serializer_class = serializers.NetworkContactSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkFacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.NetworkFacility.objects.all()
    serializer_class = serializers.NetworkFacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)


class NetworkIXLanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.NetworkIXLan.objects.all()
    serializer_class = serializers.NetworkIXLanSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PeeringRouterViewSet(viewsets.ModelViewSet):
    queryset = prngmgr_models.PeeringRouter.objects.all()
    serializer_class = serializers.PeeringRouterSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PeeringRouterIXInterfaceViewSet(viewsets.ModelViewSet):
    queryset = prngmgr_models.PeeringRouterIXInterface.objects.all()
    serializer_class = serializers.PeeringRouterIXInterfaceSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PeeringSessionViewSet(viewsets.ModelViewSet):
    queryset = prngmgr_models.PeeringSession.objects.all()
    serializer_class = serializers.PeeringSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def datatable(self, request, *args, **kwargs):
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    @list_route()
    def tabledef(self, *args, **kwargs):
        columns = [
            {'title': 'IXP',
             'data': 'ixp_name',
             'name': 'prngrtriface__netixlan__ixlan__ix__name'},
            {'title': 'Peer Name',
             'data': 'remote_network_name',
             'name': 'peer_netixlan__net__name'},
            {'title': 'Peer AS',
             'data': 'remote_network_asn',
             'name': 'peer_netixlan__asn'},
            {'title': 'Address Family',
             'data': 'address_family',
             'name': 'af'},
            {'title': 'Peer Address',
             'data': 'remote_address',
             'name': 'remote_address',
             'orderable': False,
             'searchable': False},
            {'title': 'Router',
             'data': 'router_hostname',
             'name': 'prngrtriface__prngrtr__hostname'},
            {'title': 'State',
             'data': 'session_state.display',
             'name': 'session_state.state',
             'orderable': False,
             'searchable': False},
        ]
        definition = datatables.TableDefView(columns=columns)
        return definition.response
