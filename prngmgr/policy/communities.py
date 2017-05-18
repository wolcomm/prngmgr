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
