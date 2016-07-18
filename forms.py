from django.forms import (
    ModelForm,
    BaseInlineFormSet,
    ModelChoiceField,
)
from prngmgr.models import *

class PeeringRouterForm(ModelForm):
    class Meta:
        model = PeeringRouter
        fields = ['hostname']

class PeeringRouterIXInterfaceForm(ModelForm):
    class Meta:
        model = PeeringRouterIXInterface
        fields = ['netixlan']
    netixlan = NetworkIXLanChoiceField(queryset=None)

class NetworkIXLanChoiceField(ModelChoiceField):
    def label_from_instance(self, netixlan):
        label = "%s // %s // %s" % (netixlan.ixlan.ix.name, netixlan.ipaddr4, netixlan.ipaddr6)
        return label