import re

_new_format_regex = re.compile(r'^(\d+):(\d+)$')

class StdCommunity(object):
    def __init__(self, val=None):
        try:
            m = _new_format_regex.match(val)
            if m:
                val = int(m.group(1)) * 2**16 + int(m.group(2))
        except TypeError:
            pass
        try:
            val = int(val)
        except:
            raise
        # TODO: check whether 0:0 is valid?
        if 0 < val < 2**32:
            self._val = val
        else:
            raise ValueError("Community should be a positive 32-bit integer")
