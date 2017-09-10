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

from prngmgr.policy.autnums import AutNum

_new_format_regex = re.compile(r'^(\d+):(\d+)$')


class StdCommunity(object):
    """Standard community policy object class."""

    def __init__(self, val=None):
        """Init new StdCommunity instance."""
        try:
            m = _new_format_regex.match(val)
            if m:
                a = int(m.group(1))
                if not 0 <= a < 2**16:
                    raise ValueError("ASN part of community should be a \
                                      16-bit integer")
                n = int(m.group(2))
                if not 0 <= n < 2**16:
                    raise ValueError("Numeric part of community should be a \
                                      16-bit integer")
                val = (a << 16) + n
        except TypeError:
            pass
        val = int(val)
        if 0 <= val < 2**32:
            self._val = val
        else:
            raise ValueError("Community should be a positive 32-bit integer")

    @property
    def value(self):
        """Get community value."""
        return self._val

    @property
    def as_part(self):
        """Get AS part of community."""
        return self._val >> 16

    @property
    def num_part(self):
        """Get local number part of community."""
        return self._val % 2**16

    @property
    def autnum(self):
        """Get an AutNum object corresponding to the AS part."""
        return AutNum(self.as_part)

    def __str__(self):
        """Render as string."""
        return "%s:%s" % (self.as_part, self.num_part)


class StdCommunitySet(object):
    """Standard community set policy object class."""

    def __init__(self, name=None, communities=[]):
        """Init new StdCommunitySet instance."""
        self._communities = []
        for comm in communities:
            if not isinstance(comm, StdCommunity):
                self._communities.append(StdCommunity(val=comm))
            else:
                self._communities.append(comm)

    def append(self, comm=None):
        """Append an entry to the set."""
        if isinstance(comm, StdCommunity):
            self._communities.append(comm)
        else:
            raise ValueError
