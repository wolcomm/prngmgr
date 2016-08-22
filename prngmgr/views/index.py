from django.http import HttpResponse
from django.template import loader
from django_peeringdb.models.concrete import Network
from prngmgr import settings

me = Network.objects.get(asn=settings.MY_ASN)


def index(request):
    template = loader.get_template('prngmgr/index.html')
    context = {
        'me': me,
    }
    return HttpResponse(template.render(context, request))