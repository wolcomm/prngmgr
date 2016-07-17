from django.forms import (
    ModelForm,
    BaseInlineFormSet,
)
from prngmgr.models import *

class PeeringRouterForm(ModelForm):
    class Meta:
        model = PeeringRouter
        fields = ['hostname']
