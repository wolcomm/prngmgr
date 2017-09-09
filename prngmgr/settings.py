from django.conf import settings

MY_ASN = getattr(settings, 'PRNGMGR_MY_ASN', None)

SNMP = getattr(settings, 'PRNGMGR_SNMP', {
   'port': 161,
   'user': None,
   'authPass': None,
   'privKey': None,
})
