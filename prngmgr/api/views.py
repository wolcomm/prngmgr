from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import list_route
from django_peeringdb.models import concrete as pdb_models
from prngmgr import models as prngmgr_models
from prngmgr.api import serializers, datatables


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer


class NetworkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Network.objects.all()
    serializer_class = serializers.NetworkSerializer

    @list_route()
    def datatable(self, request, *args, **kwargs):
        query_params = datatables.QueryParams(request)
        query = datatables.QueryView(
            query_set=self.queryset,
            serializer_class=self.serializer_class,
            query_params=query_params
        )
        return query.response

    # @list_route()
    # def datatable(self, request, *args, **kwargs):
    #     query = datatables.QueryParams(request).query
    #     if not query:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     page_start = query['start']
    #     page_end = page_start + query['length']
    #     base = self.queryset
    #     records_total = base.count()
    #     filter_value = query['search']['value']
    #     filter_query = Q()
    #     if filter_value:
    #         filter_cols = []
    #         for col_index in query['columns']:
    #             if query['columns'][col_index]['searchable']:
    #                 filter_cols.append(query['columns'][col_index]['name'])
    #         for col in filter_cols:
    #             filter_query |= Q(**{"%s__contains" % col: filter_value})
    #     filtered = base.filter(filter_query)
    #     records_filtered = filtered.count()
    #     order_by_columns = list()
    #     for i in query['order']:
    #         col_index = query['order'][i]['column']
    #         col_name = query['columns'][col_index]['name']
    #         if query['order'][i]['dir']:
    #             order_by_columns.append("-%s" % col_name)
    #         else:
    #             order_by_columns.append(col_name)
    #     ordered = filtered.order_by(*order_by_columns)
    #     page = ordered[page_start:page_end]
    #     serializer = self.serializer_class(page, many=True, context={'request': request})
    #     data = serializer.data
    #     response = {
    #         'draw': query['draw'],
    #         'recordsTotal': records_total,
    #         'recordsFiltered': records_filtered,
    #         'data': data,
    #     }
    #     return Response(response)


class InternetExchangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.InternetExchange.objects.all()
    serializer_class = serializers.InternetExchangeSerializer


class InternetExchangeFacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.InternetExchangeFacility.objects.all()
    serializer_class = serializers.InternetExchangeFacilitySerializer


class IXLanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.IXLan.objects.all()
    serializer_class = serializers.IXLanSerializer


class IXLanPrefixViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.IXLanPrefix.objects.all()
    serializer_class = serializers.IXLanPrefixSerializer


class NetworkContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.NetworkContact.objects.all()
    serializer_class = serializers.NetworkContactSerializer


class NetworkFacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.NetworkFacility.objects.all()
    serializer_class = serializers.NetworkFacilitySerializer


class NetworkIXLanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.NetworkIXLan.objects.all()
    serializer_class = serializers.NetworkIXLanSerializer


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
