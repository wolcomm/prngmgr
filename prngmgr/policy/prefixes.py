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
"""Prefix policy module for prngmgr."""

import ipaddress


class Prefix(object):
    """Prefix policy object class."""

    def __init__(self, prefix=None, strict=False):
        """Init new Prefix instance."""
        if isinstance(prefix, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            self._prefix = prefix
        else:
            self._prefix = ipaddress.ip_network(unicode(prefix), strict=strict)

    @property
    def prefix(self):
        """Get prefix."""
        return self._prefix


class PrefixRange(Prefix):
    """Prefix range policy object class."""

    def __init__(self, prefix=None, min_length=None, max_length=None,
                 greedy=False, strict=False):
        """Init new PrefixRange instance."""
        super(PrefixRange, self).__init__(prefix=prefix, strict=False)
        prefix_length = self.prefix.prefixlen
        if min_length is not None:
            if min_length > prefix_length:
                self._min_length = min_length
            else:
                raise ValueError("min_length should be greater \
                                  than prefix length")
        else:
            min_length = prefix_length
        if max_length is not None:
            if max_length >= min_length:
                self._max_length = max_length
            else:
                raise ValueError("max_length should be greater than or equal \
                                  to both prefix length and min_length")
        else:
            if greedy:
                self._max_length = self.prefix.max_prefixlen
            else:
                self._max_length = prefix_length


class PrefixSet(object):
    """Prefix set policy object class."""

    def __init__(self, name=None, prefixes=[]):
        """Init new PrefixSet instance."""
        self._prefixes = []
        for prefix in prefixes:
            if not isinstance(prefix, Prefix):
                self._prefixes.append(Prefix(prefix=prefix))
            else:
                self._prefixes.append(prefix)

    def append(self, p=None):
        """Append entry to PrefixSet."""
        if isinstance(p, Prefix):
            self._prefixes.append(p)
        else:
            raise ValueError
