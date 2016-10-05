from prngmgr import models


def render_alerts(calculated):
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
        elif calculated['count']['provisioned'] < calculated['count']['possible']:
            if calculated['count']['established'] < calculated['count']['provisioned']:
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
            if calculated['count']['established'] < calculated['count']['provisioned']:
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
