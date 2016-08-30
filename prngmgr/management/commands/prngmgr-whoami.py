from django.core.management.base import BaseCommand, CommandError
from prngmgr.settings import *
from prngmgr.models.models import *

class Command(BaseCommand):
    help = 'Displays infomation from our PDB record'
    def handle(self, *args, **options):
        net = Network.objects.get(asn=MY_ASN)
        self.stdout.write( "Name: %s" % net.name )
        self.stdout.write( "ASN: AS%s" % net.asn )
