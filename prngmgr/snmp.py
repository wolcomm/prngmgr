from pysnmp.hlapi import *
from prngmgr.settings import *
from prngmgr.models import *
from collections import defaultdict
from ipaddress import *

snmp = SnmpEngine()
usm = UsmUserData(SNMP['user'], SNMP['authPass'], SNMP['privKey'],
    authProtocol=usmHMACSHAAuthProtocol,
    privProtocol=usmAesCfb128Protocol)
context = ContextData()

def Get(host, oid):
    target = UdpTransportTarget((host, SNMP['port']))
    object = ObjectIdentity(oid)

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(snmp, usm, target, context, ObjectType(object))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            result = ' = '.join([x.prettyPrint() for x in varBind])
    return result

def GetBGPTable(host):
    object = ObjectIdentity('CISCO-BGP4-MIB', 'cbgpPeer2Table')
    target = UdpTransportTarget((host, SNMP['port']))

    results = defaultdict(dict)

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in bulkCmd(snmp,
                              usm,
                              target,
                              context,
                              0, 25,
                              ObjectType(object),
                              lexicographicMode=False,
                              lookupMib=True):

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
        else:
            for (key, val) in varBinds:
                (mib, name, index) = key.loadMibs('BGP4-MIB').getMibSymbol()
                (af, addr) = [ x for x in index ]
                addr = addr.prettyPrint()
                results[addr]['cbgpPeer2Type'] = af
                results[addr][name] = val
    for addr in results:
        if results[addr]['cbgpPeer2Type'] == 1:
            results[addr]['cbgpPeer2RemoteAddr'] = IPv4Address(int(addr, 16))
        if results[addr]['cbgpPeer2Type'] == 2:
            results[addr]['cbgpPeer2RemoteAddr'] = IPv6Address(int(addr, 16))
    return results

def GetTable(host, oid):
    target = UdpTransportTarget((host, SNMP['port']))
    object = ObjectIdentity(oid)

    results = []

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in bulkCmd(snmp,
                              usm,
                              target,
                              context,
                              0, 25,
                              ObjectType(object),
                              lexicographicMode=False,
                              lookupMib=True):

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
    return varBinds

