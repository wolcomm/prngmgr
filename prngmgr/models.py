from django.db import models
from django.utils import timezone
from django_handleref.models import HandleRefModel
from django_inet.models import IPAddressField
from django_peeringdb.models.concrete import *
from prngmgr import settings

ALERT_NONE = 0
ALERT_SUCCESS = 1
ALERT_WARNING = 2
ALERT_DANGER = 3


class PeeringRouterManager(models.Manager):
    def get_queryset(self):
        query_set = super(PeeringRouterManager, self).get_queryset()
        return query_set.annotate(
            peering_interfaces=models.Count('prngrtriface_set', distinct=True)
        )


class PeeringRouter(models.Model):
    objects = PeeringRouterManager()

    hostname = models.CharField(max_length=20, unique=True)

    def _local_sessions(self):
        return PeeringSession.objects.filter(prngrtriface__prngrtr=self.id)

    def _possible_sessions(self):
        return self._local_sessions().count()
    possible_sessions = property(_possible_sessions)

    def _provisioned_sessions(self):
        return self._local_sessions().filter(provisioning_state=PeeringSession.PROV_COMPLETE).count()
    provisioned_sessions = property(_provisioned_sessions)

    def _established_sessions(self):
        return self._local_sessions().filter(operational_state=PeeringSession.OPER_ESTABLISHED).count()
    established_sessions = property(_established_sessions)


class PeeringRouterIXInterface(models.Model):
    netixlan = models.OneToOneField(
        NetworkIXLan,
        default=0, related_name="prngrtriface_set", null=True,
        limit_choices_to={'net__asn': settings.MY_ASN}
    )
    prngrtr = models.ForeignKey(PeeringRouter, default=0, related_name="prngrtriface_set")


class PeeringSessionManager(models.Manager):
    def get_queryset(self):
        base_query_set = super(PeeringSessionManager, self).get_queryset()
        query_set = base_query_set.annotate(
            session_state=models.Case(
                models.When(provisioning_state=2, then=models.Case(
                    models.When(admin_state=2, then=models.Case(
                        models.When(operational_state=6, then=models.Value('Up')),
                        default=models.Value('Down')
                    )),
                    default=models.Value('Admin Down')
                )),
                models.When(provisioning_state=1, then=models.Value('Provisioning')),
                default=models.Value('None'),
                output_field=models.CharField()
            ),
            local_address=models.Case(
                models.When(af=1, then=models.F('prngrtriface__netixlan__ipaddr4')),
                models.When(af=2, then=models.F('prngrtriface__netixlan__ipaddr6')),
                default=None,
                output_field=IPAddressField()
            ),
            remote_address=models.Case(
                models.When(af=1, then=models.F('peer_netixlan__ipaddr4')),
                models.When(af=2, then=models.F('peer_netixlan__ipaddr6')),
                default=None,
                output_field=IPAddressField()
            ),
            address_family=models.Case(
                models.When(af=1, then=models.Value('IPv4')),
                models.When(af=2, then=models.Value('IPv6')),
                default=models.Value('Unknown'),
                output_field=models.CharField()
            ),
            ixp_name=models.F('prngrtriface__netixlan__ixlan__ix__name'),
            router_hostname=models.F('prngrtriface__prngrtr__hostname'),
            remote_network_name = models.F('peer_netixlan__net__name'),
            remote_network_asn = models.F('peer_netixlan__net__asn')
        )
        return query_set

    def status_summary(self):
        base_query_set = super(PeeringSessionManager, self).get_queryset()
        summary = base_query_set.annotate(
            label=models.Case(
                models.When(provisioning_state=2, then=models.Case(
                    models.When(admin_state=2, then=models.Case(
                        models.When(operational_state=6, then=models.Value('Up')),
                        default=models.Value('Down')
                    )),
                    default=models.Value('Admin Down')
                )),
                models.When(provisioning_state=1, then=models.Value('Provisioning')),
                default=models.Value('None'),
                output_field=models.CharField()
            )).values('label').annotate(value=models.Count('label'))
        return summary


class PeeringSession(models.Model):
    objects = PeeringSessionManager()

    PROV_NONE = 0
    PROV_PENDING = 1
    PROV_COMPLETE = 2
    PROV_OPTIONS = (
        (PROV_NONE, None),
        (PROV_PENDING, 'pending'),
        (PROV_COMPLETE, 'complete'),
    )
    provisioning_state = models.IntegerField(choices=PROV_OPTIONS, default=PROV_NONE)

    def _get_provisioning_state_alert(self):
        if self.provisioning_state == self.PROV_COMPLETE:
            return ALERT_SUCCESS
        elif self.provisioning_state == self.PROV_PENDING:
            return ALERT_WARNING
        else:
            return ALERT_NONE
    get_provisioning_state_alert = property(_get_provisioning_state_alert)

    ADMIN_NONE = 0
    ADMIN_STOP = 1
    ADMIN_START = 2
    ADMIN_OPTIONS = (
        (ADMIN_NONE, None),
        (ADMIN_STOP, 'stop'),
        (ADMIN_START, 'start'),
    )
    admin_state = models.IntegerField(choices=ADMIN_OPTIONS, default=ADMIN_NONE)

    def _get_admin_state_alert(self):
        if self.admin_state == self.ADMIN_START:
            return ALERT_SUCCESS
        elif self.admin_state == self.ADMIN_STOP:
            return ALERT_DANGER
        else:
            return ALERT_NONE
    get_admin_state_alert = property(_get_admin_state_alert)

    OPER_NONE = 0
    OPER_IDLE = 1
    OPER_CONNECT = 2
    OPER_ACTIVE = 3
    OPER_OPENSENT = 4
    OPER_OPENCONFIRM = 5
    OPER_ESTABLISHED = 6
    OPER_OPTIONS = (
        (OPER_NONE, None),
        (OPER_IDLE, "idle"),
        (OPER_CONNECT, "connect"),
        (OPER_ACTIVE, "active"),
        (OPER_OPENSENT, "opensent"),
        (OPER_OPENCONFIRM, "openconfirm"),
        (OPER_ESTABLISHED, "established"),
    )
    operational_state = models.IntegerField(choices=OPER_OPTIONS, default=OPER_NONE)

    def _get_operational_state_alert(self):
        if self.operational_state == self.OPER_ESTABLISHED:
            return ALERT_SUCCESS
        elif self.operational_state == self.OPER_NONE:
            return ALERT_NONE
        else:
            return ALERT_DANGER
    get_operational_state_alert = property(_get_operational_state_alert)

    AF_UNKNOWN = 0
    AF_IPV4 = 1
    AF_IPV6 = 2
    AF_OPTIONS = (
        (AF_UNKNOWN, 'unknown'),
        (AF_IPV4, 'ipv4'),
        (AF_IPV6, 'ipv6'),
    )
    af = models.IntegerField(choices=AF_OPTIONS, default=AF_UNKNOWN)

    accepted_prefixes = models.IntegerField(null=True, default=None)
    previous_state = models.CharField(max_length=12, default='None')
    state_changed = models.DateTimeField(default=timezone.now)
    peer_netixlan = models.ForeignKey(NetworkIXLan, default=0, related_name="prngsess_set", null=True)
    prngrtriface = models.ForeignKey(PeeringRouterIXInterface, default=0, related_name="prngsess_set")

    class Meta:
        unique_together = ("af", "prngrtriface", "peer_netixlan")


class InternetExchangeProxyManager(models.Manager):
    def get_queryset(self):
        query_set = super(InternetExchangeProxyManager, self).get_queryset()
        return query_set.annotate(
            participants=models.Count('ixlan_set__netixlan_set__asn', distinct=True),
        )


class InternetExchangeProxy(InternetExchange):
    class Meta:
        proxy = True

    objects = InternetExchangeProxyManager()

    def _local_sessions(self):
        return PeeringSession.objects.filter(peer_netixlan__ixlan__ix=self.id)

    def _possible_sessions(self):
        return self._local_sessions().count()
    possible_sessions = property(_possible_sessions)

    def _provisioned_sessions(self):
        return self._local_sessions().filter(provisioning_state=PeeringSession.PROV_COMPLETE).count()
    provisioned_sessions = property(_provisioned_sessions)

    def _established_sessions(self):
        return self._local_sessions().filter(operational_state=PeeringSession.OPER_ESTABLISHED).count()
    established_sessions = property(_established_sessions)


class NetworkProxyManager(models.Manager):
    def get_queryset(self):
        query_set = super(NetworkProxyManager, self).get_queryset()
        return query_set


class NetworkProxy(Network):
    class Meta:
        proxy = True

    objects = NetworkProxyManager()

    def _local_sessions(self):
        return PeeringSession.objects.filter(peer_netixlan__net=self.id)

    def _possible_sessions(self):
        return self._local_sessions().count()
    possible_sessions = property(_possible_sessions)

    def _provisioned_sessions(self):
        return self._local_sessions().filter(provisioning_state=PeeringSession.PROV_COMPLETE).count()
    provisioned_sessions = property(_provisioned_sessions)

    def _established_sessions(self):
        return self._local_sessions().filter(operational_state=PeeringSession.OPER_ESTABLISHED).count()
    established_sessions = property(_established_sessions)
