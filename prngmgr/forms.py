from django.forms import ModelForm, ModelChoiceField, CharField
from django.forms.widgets import TextInput, HiddenInput
from django_peeringdb.models import concrete as pdb_models
from prngmgr import models
from prngmgr.settings import *


class NetworkIXLanHiddenWidget(TextInput):
    def __init__(self, attrs=None):
        if attrs:
            attrs.update(hidden=True)
        else:
            attrs = dict(hidden=True)
        super(NetworkIXLanHiddenWidget,self).__init__(attrs)

    def render(self, name, value, attrs=None):
        netixlan = pdb_models.NetworkIXLan.objects.get(id=value)
        label = "%s ( %s // %s )" % (netixlan.ixlan.ix.name, netixlan.ipaddr4, netixlan.ipaddr6)
        html = "%s<i>%s</i>" % (
            super(NetworkIXLanHiddenWidget, self).render(name, value, attrs),
            label
        )
        return html

class NetworkIXLanChoiceField(ModelChoiceField):
    def label_from_instance(self, netixlan):
        label = "%s ( %s // %s )" % (netixlan.ixlan.ix.name, netixlan.ipaddr4, netixlan.ipaddr6)
        return label

class PeeringRouterForm(ModelForm):
    class Meta:
        model = models.PeeringRouter
        fields = ['hostname']

class PeeringRouterIXInterfaceForm(ModelForm):
    netixlan = CharField(
        label='IXP Interface',
        widget=NetworkIXLanHiddenWidget
    )
    class Meta:
        model = models.PeeringRouterIXInterface
        fields = ['prngrtr', 'netixlan']
        widgets = {
            'prngrtr': HiddenInput,
        }

class NewPeeringRouterIXInterfaceForm(PeeringRouterIXInterfaceForm):
    available = pdb_models.NetworkIXLan.objects.filter(
        net__asn=MY_ASN
    ).exclude(
        id__in=models.PeeringRouterIXInterface.objects.all().values('netixlan')
    )
    netixlan = NetworkIXLanChoiceField(
        queryset=available,
        # queryset=NetworkIXLan.objects.filter(net__asn=MY_ASN),
        label='IXP Interface'
    )