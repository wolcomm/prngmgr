from django.core.management.base import BaseCommand
from prngmgr import models
from prngmgr.settings import *


class Command(BaseCommand):
    help = 'Displays infomation from our PDB record'
    def handle(self, *args, **options):
        net = models.Network.objects.get(asn=MY_ASN)
        self.stdout.write( "Name: %s" % net.name )
        self.stdout.write( "ASN: AS%s" % net.asn )
