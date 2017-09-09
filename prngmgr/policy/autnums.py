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
"""Autnum policy module for prngmgr."""

import re

_as_regex = re.compile(r'^AS(\d+)$')
_asdot_regex = re.compile(r'^(\d+)\.(\d+)$')


class AutNum(object):
    def __init__(self, asn=None):
        try:
            m = _as_regex.match(asn)
            if m:
                asn = m.group(1)
            m = _asdot_regex.match(asn)
            if m:
                asn = int(m.group(1)) * 2**16 + int(m.group(2))
        except TypeError:
            pass
        try:
            asn = int(asn)
        except:
            raise
        if 0 < asn < 2 ** 32:
            self._autnum = asn
        else:
            raise ValueError("ASN must be a postive 32-bit integer")

    @property
    def autnum(self):
        return self._autnum

    @property
    def is_4byte(self):
        if self.autnum < 2**16:
            return False
        else:
            return True

    def __str__(self):
        return str(self.autnum)

    def __unicode__(self):
        return self.__str__()
