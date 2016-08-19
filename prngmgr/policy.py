import ipaddress
from django.template import loader
from prngmgr import models


class Prefix(object):
    def __init__(self, prefix=None, strict=False):
        if isinstance(prefix, ipaddress.IPv4Network):
            self._prefix = prefix
        elif isinstance(prefix, ipaddress.IPv6Network):
            self._prefix = prefix
        else:
            try:
                self._prefix = ipaddress.ip_network(prefix, strict=strict)
            except:
                raise

    @property
    def prefix(self):
        return self._prefix


class PrefixRange(Prefix):
    def __init__(self, min_length=None, max_length=None, greedy=False, **kwargs):
        super(PrefixRange, self).__init__(**kwargs)
        prefix_length = self.prefix.prefixlen
        if min_length is not None:
            if min_length > prefix_length:
                self._min_length = min_length
            else:
                raise ValueError("min_length should be greater than prefix length")
        else:
            min_length = prefix_length
        if max_length is not None:
            if max_length >= min_length:
                self._max_length = max_length
            else:
                raise ValueError("max_length should be greater than or equal to both prefix length and min_length")
        else:
            if greedy:
                self._max_length = self.prefix.max_prefixlen
            else:
                self._max_length = prefix_length


class PrefixSet(object):
    def __init__(self, name=None, prefixes=[]):
        self._prefixes = []
        for prefix in prefixes:
            if not isinstance(prefix, Prefix):
                try:
                    self._prefixes.append(Prefix(prefix=prefix))
                except:
                    raise
            else:
                self._prefixes.append(prefix)

    def append(self, p=None):
        if isinstance(p, Prefix):
            self._prefixes.append(p)
        else:
            raise ValueError
