import ipaddress
from pysnmp.hlapi import *
from pysnmp.proto.rfc1905 import EndOfMibView
from prngmgr.settings import SNMP
from prngmgr.models.models import *
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
                    (af, addr) = [x for x in index]
                    addr = addr.prettyPrint()
                    results[addr]['cbgpPeer2Type'] = af
                    results[addr][name] = val
    for addr in results:
        if results[addr]['cbgpPeer2Type'] == 1:
            results[addr]['cbgpPeer2RemoteAddr'] = ipaddress.IPv4Network(int(addr, 16))
        if results[addr]['cbgpPeer2Type'] == 2:
            results[addr]['cbgpPeer2RemoteAddr'] = ipaddress.IPv6Address(int(addr, 16))
    return results

# def Get(host, oid):
#     target = UdpTransportTarget((host, SNMP['port']))
#     obj = ObjectIdentity(oid)
#
#     errorIndication, errorStatus, errorIndex, varBinds = next(
#         getCmd(snmp, usm, target, context, ObjectType(obj))
#     )
#
#     if errorIndication:
#         print(errorIndication)
#     elif errorStatus:
#         print('%s at %s' % (errorStatus.prettyPrint(),
#                             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#     else:
#         for varBind in varBinds:
#             result = ' = '.join([x.prettyPrint() for x in varBind])
#     return result
#
#
# def GetTable(host, oid):
#     target = UdpTransportTarget((host, SNMP['port']))
#     obj = ObjectIdentity(oid)
#
#     results = []
#
#     for (errorIndication,
#          errorStatus,
#          errorIndex,
#          varBinds) in bulkCmd(snmp,
#                               usm,
#                               target,
#                               context,
#                               0, 25,
#                               ObjectType(obj),
#                               lexicographicMode=False,
#                               lookupMib=True):
#
#         if errorIndication:
#             print(errorIndication)
#         elif errorStatus:
#             print('%s at %s' % (errorStatus.prettyPrint(),
#                                 errorIndex and varBinds[-1][int(errorIndex)-1] or '?'))
#         else:
#             for varBind in varBinds:
#                 print(' = '.join([x.prettyPrint() for x in varBind]))
#     return varBinds
#
