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
"""Serializers module for prngmgr API."""

from django_countries.serializer_fields import CountryField

from django_inet.rest import IPAddressField

from django_peeringdb.models import concrete as pdb_models

from prngmgr import models as prngmgr_models

from rest_framework import serializers


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """Organization serializer class."""

    country = CountryField()

    class Meta:
        """Meta class."""

        model = pdb_models.Organization


class FacilitySerializer(serializers.HyperlinkedModelSerializer):
    """Facility serializer class."""

    country = CountryField()

    class Meta:
        """Meta class."""

        model = pdb_models.Facility


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    """Network serializer class."""

    class Meta:
        """Meta class."""

        model = prngmgr_models.NetworkProxy
        fields = ('name', 'asn', 'irr_as_set', 'looking_glass',
                  'policy_general', 'possible_sessions',
                  'provisioned_sessions', 'established_sessions')


class InternetExchangeSerializer(serializers.HyperlinkedModelSerializer):
    """IXP serializer class."""

    country = CountryField()
    participants = serializers.IntegerField()

    class Meta:
        """Meta class."""

        model = prngmgr_models.InternetExchangeProxy
        fields = ('name', 'country', 'region_continent', 'participants',
                  'possible_sessions', 'provisioned_sessions',
                  'established_sessions', 'name_long', 'city', 'notes')


class InternetExchangeFacilitySerializer(
        serializers.HyperlinkedModelSerializer):
    """IXP Facility serializer class."""

    class Meta:
        """Meta class."""

        model = pdb_models.InternetExchangeFacility


class IXLanSerializer(serializers.HyperlinkedModelSerializer):
    """IXP LAN serializer class."""

    class Meta:
        """Meta class."""

        model = pdb_models.IXLan


class IXLanPrefixSerializer(serializers.HyperlinkedModelSerializer):
    """IXP LAN Prefix serializer class."""

    class Meta:
        """Meta class."""

        model = pdb_models.IXLanPrefix


class NetworkContactSerializer(serializers.HyperlinkedModelSerializer):
    """Network contact serializer class."""

    class Meta:
        """Meta class."""

        model = pdb_models.NetworkContact


class NetworkFacilitySerializer(serializers.HyperlinkedModelSerializer):
    """Network facility serializer class."""

    class Meta:
        """Meta class."""

        model = pdb_models.NetworkFacility


class NetworkIXLanSerializer(serializers.HyperlinkedModelSerializer):
    """Network IXP LAN serializer class."""

    class Meta:
        """Meta class."""

        model = pdb_models.NetworkIXLan


class PeeringRouterSerializer(serializers.HyperlinkedModelSerializer):
    """Peering router serializer class."""

    peering_interfaces = serializers.IntegerField()

    class Meta:
        """Meta class."""

        model = prngmgr_models.PeeringRouter
        fields = ('hostname', 'peering_interfaces', 'possible_sessions',
                  'provisioned_sessions', 'established_sessions')


class PeeringRouterIXInterfaceSerializer(
        serializers.HyperlinkedModelSerializer):
    """Peering router IXP interface serializer class."""

    class Meta:
        """Meta class."""

        model = prngmgr_models.PeeringRouterIXInterface


class PeeringSessionSerializer(serializers.HyperlinkedModelSerializer):
    """Peering session serializer class."""

    session_class = serializers.SerializerMethodField()
    session_state = serializers.CharField()
    address_family = serializers.CharField()
    local_address = IPAddressField()
    remote_address = IPAddressField()
    ixp_name = serializers.CharField()
    router_hostname = serializers.CharField()
    remote_network_name = serializers.CharField()
    remote_network_asn = serializers.IntegerField()

    def get_session_class(self, obj):
        """Get css class according to session state."""
        if obj.session_state == 'Up':
            return 'success'
        elif obj.session_state == 'Down':
            return 'danger'
        elif obj.session_state == 'Admin Down':
            return 'warning'
        elif obj.session_state == 'Provisioning':
            return 'info'
        else:
            return None

    class Meta:
        """Meta class."""

        model = prngmgr_models.PeeringSession
        fields = ('provisioning_state', 'admin_state', 'operational_state',
                  'session_state', 'session_class', 'af', 'address_family',
                  'peer_netixlan', 'prngrtriface', 'local_address',
                  'remote_address', 'ixp_name', 'router_hostname',
                  'remote_network_name', 'remote_network_asn',
                  'accepted_prefixes', 'previous_state', 'state_changed')
