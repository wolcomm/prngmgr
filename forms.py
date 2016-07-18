from django.forms import (
    ModelForm,
    BaseInlineFormSet,
    ModelChoiceField,
)
from prngmgr.models import *
from prngmgr.settings import *

class NetworkIXLanChoiceField(ModelChoiceField):
    def label_from_instance(self, netixlan):
        label = "%s // %s // %s" % (netixlan.ixlan.ix.name, netixlan.ipaddr4, netixlan.ipaddr6)
        return label

class PeeringRouterForm(ModelForm):
    class Meta:
        model = PeeringRouter
        fields = ['hostname']

class PeeringRouterIXInterfaceForm(ModelForm):
    netixlan = NetworkIXLanChoiceField(queryset=NetworkIXLan.objects.filter(net__asn=MY_ASN))
    class Meta:
        model = PeeringRouterIXInterface
        fields = ['netixlan']
