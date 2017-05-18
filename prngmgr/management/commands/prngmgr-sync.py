from django.core.management.base import BaseCommand, CommandError
from django.core import management

class Command(BaseCommand):
    help = 'Helper command to sync PDB and PrngMgr data'
    def handle(self, *args, **options):
        self.stdout.write( self.style.NOTICE('Syncing PDB') )
        management.call_command('pdb_sync')
        self.stdout.write( self.style.NOTICE('Rebuilding session data') )
        management.call_command('prngmgr-sync-sessions', *args, **options)
        self.stdout.write( self.style.NOTICE('Sync complete') )
