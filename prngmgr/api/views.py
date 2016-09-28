from rest_framework import permissions
from rest_framework import viewsets
from django_peeringdb.models import concrete as pdb_models
from prngmgr import models as prngmgr_models
from prngmgr.api import serializers


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer


class NetworkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pdb_models.Network.objects.all()
    serializer_class = serializers.NetworkSerializer


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
