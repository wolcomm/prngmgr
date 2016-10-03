from django.db.models import Count
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from django_inet.rest import IPAddressField
from django_peeringdb.models import concrete as pdb_models
from prngmgr import models as prngmgr_models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()

    class Meta:
        model = pdb_models.Organization


class FacilitySerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()

    class Meta:
        model = pdb_models.Facility


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = prngmgr_models.NetworkProxy
        fields = ('name', 'asn', 'irr_as_set', 'looking_glass', 'policy_general',
                  'possible_sessions', 'provisioned_sessions', 'established_sessions')


class InternetExchangeSerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()
    participants = serializers.IntegerField()

    class Meta:
        model = prngmgr_models.InternetExchangeProxy
        fields = ('name', 'country', 'region_continent', 'participants',
                  'possible_sessions', 'provisioned_sessions', 'established_sessions',
                  'name_long', 'city', 'notes')


class InternetExchangeFacilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pdb_models.InternetExchangeFacility


class IXLanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pdb_models.IXLan


class IXLanPrefixSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pdb_models.IXLanPrefix


class NetworkContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pdb_models.NetworkContact


class NetworkFacilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pdb_models.NetworkFacility


class NetworkIXLanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pdb_models.NetworkIXLan


class PeeringRouterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = prngmgr_models.PeeringRouter


class PeeringRouterIXInterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = prngmgr_models.PeeringRouterIXInterface


class PeeringSessionSerializer(serializers.HyperlinkedModelSerializer):
    local_address = IPAddressField()
    remote_address = IPAddressField()

    class Meta:
        model = prngmgr_models.PeeringSession
        fields = ('provisioning_state', 'admin_state', 'operational_state',
                  'af', 'peer_netixlan', 'prngrtriface', 'local_address', 'remote_address',
                  'ixp_name', 'router_hostname', 'remote_network_name', 'remote_network_asn')
