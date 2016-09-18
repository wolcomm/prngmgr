import ipaddress
from pysnmp.hlapi import *
from pysnmp.proto.rfc1905 import EndOfMibView
from prngmgr.settings import SNMP
# from prngmgr.models.models import *
from collections import defaultdict


snmp = SnmpEngine()
usm = UsmUserData(
    SNMP['user'], SNMP['authPass'], SNMP['privKey'],
    authProtocol=usmHMACSHAAuthProtocol,
    privProtocol=usmAesCfb128Protocol
)
context = ContextData()


def get_bgp_table(host):
    obj = ObjectIdentity('CISCO-BGP4-MIB', 'cbgpPeer2Table')
    target = UdpTransportTarget((host, SNMP['port']))

    results = defaultdict(dict)

    for (errorIndication, errorStatus,
         errorIndex, varBinds) in bulkCmd(snmp, usm, target, context, 0, 25, ObjectType(obj),
                                          lexicographicMode=False, lookupMib=True):
        if errorIndication:
            raise RuntimeError(errorIndication)
        elif errorStatus:
            raise RuntimeError('%s at %s' % (errorStatus.prettyPrint(),
                                             errorIndex and varBinds[-1][int(errorIndex)-1] or '?'))
        else:
            for (key, val) in varBinds:
                if not isinstance(val, EndOfMibView):
                    (mib, name, index) = key.loadMibs('BGP4-MIB').getMibSymbol()
                    a = index[1].prettyPrint()
                    results[a]['cbgpPeer2Type'] = index[0]
                    results[a][name] = val
    for address in results:
        if results[address]['cbgpPeer2Type'] == 1:
            results[address]['cbgpPeer2RemoteAddr'] = ipaddress.IPv4Address(int(address, 16))
        elif results[address]['cbgpPeer2Type'] == 2:
            results[address]['cbgpPeer2RemoteAddr'] = ipaddress.IPv6Address(int(address, 16))
    return results
