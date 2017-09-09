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
"""Community policy module for prngmgr."""

import re
import collections
from prngmgr.policy.autnums import AutNum

_new_format_regex = re.compile(r'^(\d+):(\d+)$')


class StdCommunity(object):
    def __init__(self, val=None):
        try:
            m = _new_format_regex.match(val)
            if m:
                a = int(m.group(1))
                if not 0 <= a < 2**16:
                    raise ValueError("ASN part of community should be a 16-bit integer")
                n = int(m.group(2))
                if not 0 <= n < 2**16:
                    raise ValueError("Numeric part of community should be a 16-bit integer")
                val = (a << 16) + n
        except TypeError:
            pass
        try:
            val = int(val)
        except:
            raise
        if 0 <= val < 2**32:
            self._val = val
        else:
            raise ValueError("Community should be a positive 32-bit integer")

    @property
    def value(self):
        return self._val

    @property
    def as_part(self):
        return self._val >> 16

    @property
    def num_part(self):
        return self._val % 2**16

    @property
    def autnum(self):
        return AutNum(self.as_part)

    def __str__(self):
        return "%s:%s" % (self.as_part, self.num_part)


class StdCommunitySet(object):
    def __init__(self, name=None, communities=[]):
        self._communities = []
        for comm in communities:
            if not isinstance(comm, StdCommunity):
                try:
                    self._communities.append(StdCommunity(val=comm))
                except:
                    raise
            else:
                self._communities.append(comm)

    def append(self, comm=None):
        if isinstance(comm, StdCommunity):
            self._communities.append(comm)
        else:
            raise ValueError
