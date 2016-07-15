from django.contrib import admin
from django.forms import ModelChoiceField
from django_peeringdb.models.concrete import *
from prngmgr.models import PeeringRouter, PeeringRouterIXInterface
from prngmgr.settings import *

class NetworkIXLanChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        ix_name = obj.ixlan.ix.name
        ipaddr4 = obj.ipaddr4
        ipaddr6 = obj.ipaddr6
        return "%s - %s // %s" % (ix_name, ipaddr4, ipaddr6)

class PeeringRouterIXInterfaceInLine(admin.TabularInline):
    model = PeeringRouterIXInterface
    fields = ['netixlan']
    extra = 1
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "netixlan":
            me = Network.objects.get(asn=MY_ASN)
            kwargs["queryset"] = NetworkIXLan.objects.filter(net=me)
            return NetworkIXLanChoiceField(**kwargs)
        return super(PeeringRouterIXInterfaceInLine, self).formfield_for_foreignkey(db_field, request, **kwargs)

class PeeringRouterAdmin(admin.ModelAdmin):
    list_display = ['hostname']
    fields = ['hostname']
    inlines = [PeeringRouterIXInterfaceInLine]

admin.site.register(PeeringRouter, PeeringRouterAdmin)
