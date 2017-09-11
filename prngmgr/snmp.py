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
"""SNMP module for prngmgr."""

import ipaddress

from collections import defaultdict

from prngmgr.settings import SNMP

from pysnmp.hlapi import (
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    UsmUserData,
    bulkCmd,
    usmAesCfb128Protocol,
    usmHMACSHAAuthProtocol,
)
from pysnmp.proto.rfc1905 import EndOfMibView


snmp = SnmpEngine()
usm = UsmUserData(
    SNMP['user'], SNMP['authPass'], SNMP['privKey'],
    authProtocol=usmHMACSHAAuthProtocol,
    privProtocol=usmAesCfb128Protocol
)
context = ContextData()


def get_bgp_table(host):
    """Return the contents of the cbgpPeer2Table table."""
    obj = ObjectIdentity('CISCO-BGP4-MIB', 'cbgpPeer2Table')
    target = UdpTransportTarget((host, SNMP['port']))

    results = defaultdict(dict)

    for (errorIndication, errorStatus,
         errorIndex, varBinds) in bulkCmd(snmp, usm, target, context, 0, 25,
                                          ObjectType(obj),
                                          lexicographicMode=False,
                                          lookupMib=True):
        if errorIndication:
            raise RuntimeError(errorIndication)
        elif errorStatus:
            raise RuntimeError('%s at %s'
                               % (errorStatus.prettyPrint(),
                                  errorIndex
                                  and varBinds[-1][int(errorIndex)-1] or '?'))
        else:
            for (key, val) in varBinds:
                if not isinstance(val, EndOfMibView):
                    (mib, name, index) = \
                        key.loadMibs('BGP4-MIB').getMibSymbol()
                    a = index[1].prettyPrint()
                    results[a]['cbgpPeer2Type'] = index[0]
                    results[a][name] = val
    for address in results:
        if results[address]['cbgpPeer2Type'] == 1:
            results[address]['cbgpPeer2RemoteAddr'] = \
                ipaddress.IPv4Address(int(address, 16))
        elif results[address]['cbgpPeer2Type'] == 2:
            results[address]['cbgpPeer2RemoteAddr'] = \
                ipaddress.IPv6Address(int(address, 16))
    return results


def get_bgp_state(host):  # noqa
    """Get the BGP session state."""
    peer_table = ObjectIdentity('CISCO-BGP4-MIB', 'cbgpPeer2Table')
    af_table = ObjectIdentity('CISCO-BGP4-MIB', 'cbgpPeer2AddrFamilyTable')
    prefix_table = ObjectIdentity('CISCO-BGP4-MIB',
                                  'cbgpPeer2AddrFamilyPrefixTable')
    target = UdpTransportTarget((host, SNMP['port']))

    results = defaultdict(dict)

    for (errorIndication, errorStatus,
         errorIndex, varBinds) in bulkCmd(snmp, usm, target, context, 0, 25,
                                          ObjectType(peer_table),
                                          lexicographicMode=False,
                                          lookupMib=True):
        if errorIndication:
            raise RuntimeError(errorIndication)
        elif errorStatus:
            raise RuntimeError('%s at %s'
                               % (errorStatus.prettyPrint(),
                                  errorIndex
                                  and varBinds[-1][int(errorIndex)-1] or '?'))
        else:
            for (key, val) in varBinds:
                if not isinstance(val, EndOfMibView):
                    (mib, name, index) = \
                        key.loadMibs('BGP4-MIB').getMibSymbol()
                    address = index[1].prettyPrint()
                    results[address]['cbgpPeer2Type'] = index[0]
                    results[address][name] = val
    for address in results:
        results[address]['address_families'] = defaultdict(dict)
    for (errorIndication, errorStatus,
         errorIndex, varBinds) in bulkCmd(snmp, usm, target, context, 0, 25,
                                          ObjectType(af_table),
                                          lexicographicMode=False,
                                          lookupMib=True):
        if errorIndication:
            raise RuntimeError(errorIndication)
        elif errorStatus:
            raise RuntimeError('%s at %s'
                               % (errorStatus.prettyPrint(),
                                  errorIndex
                                  and varBinds[-1][int(errorIndex)-1] or '?'))
        else:
            for (key, val) in varBinds:
                if not isinstance(val, EndOfMibView):
                    (mib, name, index) = \
                        key.loadMibs('BGP4-MIB').getMibSymbol()
                    address = index[1].prettyPrint()
                    afi = index[2]
                    safi = index[3]
                    results[address]['address_families'][afi][safi] = \
                        {name: val}
    for (errorIndication, errorStatus,
         errorIndex, varBinds) in bulkCmd(snmp, usm, target, context, 0, 25,
                                          ObjectType(prefix_table),
                                          lexicographicMode=False,
                                          lookupMib=True):
        if errorIndication:
            raise RuntimeError(errorIndication)
        elif errorStatus:
            raise RuntimeError('%s at %s'
                               % (errorStatus.prettyPrint(),
                                  errorIndex
                                  and varBinds[-1][int(errorIndex)-1] or '?'))
        else:
            for (key, val) in varBinds:
                if not isinstance(val, EndOfMibView):
                    (mib, name, index) = \
                        key.loadMibs('BGP4-MIB').getMibSymbol()
                    address = index[1].prettyPrint()
                    afi = index[2]
                    safi = index[3]
                    results[address]['address_families'][afi][safi][name] = \
                        val
    for address in results:
        if results[address]['cbgpPeer2Type'] == 1:
            results[address]['cbgpPeer2RemoteAddr'] = \
                ipaddress.IPv4Address(int(address, 16))
        elif results[address]['cbgpPeer2Type'] == 2:
            results[address]['cbgpPeer2RemoteAddr'] = \
                ipaddress.IPv6Address(int(address, 16))
        results[address]['TotalAcceptedPrefixes'] = 0
        for afi in results[address]['address_families']:
            for safi in results[address]['address_families'][afi]:
                results[address]['TotalAcceptedPrefixes'] += \
                    results[address]['address_families'][afi][safi]['cbgpPeer2AcceptedPrefixes']  # noqa
    return results
