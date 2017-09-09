# Copyright 2016-2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Management command module for prngmgr."""

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
