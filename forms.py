from django.forms import ModelForm
from prngmgr.models import *

class PeeringRouterForm(ModelForm):
    class Meta:
        model = PeeringRouter
        fields = ['hostname']
