from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseNotAllowed
from django_peeringdb.models.concrete import Network
from prngmgr import settings, forms, models

me = Network.objects.get(asn=settings.MY_ASN)


@login_required
def interfaces(request, if_id, if_delete):
    if request.method == 'POST':
        if if_id:
            if_id = int(if_id)
            if if_id == 0:
                form = forms.PeeringRouterIXInterfaceForm(request.POST)
            else:
                try:
                    interface = models.PeeringRouterIXInterface.objects.get(id=if_id)
                except:
                    return HttpResponseNotFound(if_id)
                if if_delete:
                    router = interface.prngrtr
                    models.PeeringRouterIXInterface.objects.filter(id=if_id).delete()
                    return HttpResponseRedirect(reverse('prngmgr-routers', kwargs={'rtr_id': router.id}))
                form = forms.PeeringRouterIXInterfaceForm(request.POST, instance=interface)
            interface = form.save()
            router = interface.prngrtr
            return HttpResponseRedirect(reverse('prngmgr-routers', kwargs = { 'rtr_id': router.id }))
        else:
            return HttpResponseRedirect(reverse('prngmgr-routers'))
    else:
        return HttpResponseNotAllowed(['POST'])
