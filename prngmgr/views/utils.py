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
"""View utilities module for prngmgr."""

from prngmgr import models


def render_alerts(calculated):
    """Render alerts dict."""
    if calculated['count']['possible'] == 0:
        calculated['alert'] = {
            'possible': models.ALERT_NONE,
            'provisioned': models.ALERT_NONE,
            'established': models.ALERT_NONE,
        }
    else:
        if calculated['count']['provisioned'] == 0:
            calculated['alert'] = {
                'possible': models.ALERT_SUCCESS,
                'provisioned': models.ALERT_DANGER,
                'established': models.ALERT_DANGER,
            }
        elif calculated['count']['provisioned'] < calculated['count']['possible']:  # noqa
            if calculated['count']['established'] < calculated['count']['provisioned']:  # noqa
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_WARNING,
                    'established': models.ALERT_DANGER,
                }
            else:
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_WARNING,
                    'established': models.ALERT_WARNING,
                }
        else:
            if calculated['count']['established'] < calculated['count']['provisioned']:  # noqa
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_SUCCESS,
                    'established': models.ALERT_DANGER,
                }
            else:
                calculated['alert'] = {
                    'possible': models.ALERT_SUCCESS,
                    'provisioned': models.ALERT_SUCCESS,
                    'established': models.ALERT_SUCCESS,
                }
    return calculated
