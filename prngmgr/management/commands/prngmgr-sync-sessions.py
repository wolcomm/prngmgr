from collections import Counter
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from prngmgr import models, settings
from napalm_base import get_network_driver


class Command(BaseCommand):
    help = 'Queries peering routers for BGP neighbour information'

    def add_arguments(self, parser):
        parser.add_argument(
            '--router',
            action='store',
            dest='router',
            default=False,
            help='Query specified router only',
        )

    def handle(self, *args, **options):

        # find our Network object
        me = models.Network.objects.get(asn=settings.MY_ASN)

        # select which vrf to look for bgp sessions in
        vrf = 'global'

        # create list of PeeringRouters and a totals counter
        rtrs = []
        totals = Counter()

        if options['router']:
            # check if we were given a router to query
            try:
                rtr = models.PeeringRouter.objects.get(hostname=options['router'])
            except models.PeeringRouter.DoesNotExist:
                raise CommandError('PeeringRouter "%s" does not exist' % options['router'])
            rtrs.append(rtr)
        else:
            # fallback to querying all PeeringRouters
            for rtr in models.PeeringRouter.objects.all():
                rtrs.append(rtr)

        for rtr in rtrs:

            # create per router counter and update rtr count
            count = Counter()
            totals['rtrs'] += 1

            # try get bgp neighbors
            self.stdout.write("Querying %s using napalm" % rtr.hostname)
            try:
                driver = get_network_driver(rtr.driver)
                device = driver(hostname=rtr.hostname, **settings.NAPALM)
                device.open()
                bgp_neighbors = device.get_bgp_neighbors()
                device.close()
            except Exception:
                raise

            if bgp_neighbors:
                try:
                    peers = bgp_neighbors[vrf]['peers']
                except KeyError:
                    peers = {}
            else:
                peers = {}

            # get all PeeringRouterIXInterfaces on router
            ifaces = models.PeeringRouterIXInterface.objects.filter(prngrtr=rtr)
            for iface in ifaces:

                # update count
                count['prngrtrifaces'] += 1

                # get all NetworkIXLans on a common IX
                peer_netixlans = models.NetworkIXLan.objects.filter(ixlan=iface.netixlan.ixlan)
                for peer_netixlan in peer_netixlans:

                    # check that we're not peering with ourselves
                    if peer_netixlan.net == me:
                        continue

                    # check for valid ipv4 peering info
                    if iface.netixlan.ipaddr4 and peer_netixlan.ipaddr4:

                        # update count
                        count['prngsess4'] += 1

                        prngsess, new = models.PeeringSession.objects.get_or_create(
                            af=models.PeeringSession.AF_IPV4,
                            peer_netixlan=peer_netixlan,
                            prngrtriface=iface
                        )

                        if new:
                            count['newsess4'] += 1

                        if str(prngsess.peer_netixlan.ipaddr4) in peers:
                            count['bgpprng4'] += 1
                            bgpprng = peers[str(prngsess.peer_netixlan.ipaddr4)]
                        else:
                            bgpprng = None

                        # update PeeringSession from bgp peering state
                        self._update_state(prngsess, bgpprng)

                        # save and move on
                        prngsess.save()

                    # check for valid ipv6 peering info
                    if iface.netixlan.ipaddr6 and peer_netixlan.ipaddr6:

                        # update count
                        count['prngsess6'] += 1

                        prngsess, new = models.PeeringSession.objects.get_or_create(
                            af=models.PeeringSession.AF_IPV6,
                            peer_netixlan=peer_netixlan,
                            prngrtriface=iface
                        )

                        if new:
                            count['newsess6'] += 1

                        if str(prngsess.peer_netixlan.ipaddr6) in peers:
                            count['bgpprng6'] += 1
                            bgpprng = peers[str(prngsess.peer_netixlan.ipaddr6)]
                        else:
                            bgpprng = None

                        # update PeeringSession from bgp peering state
                        self._update_state(prngsess, bgpprng)

                        # save and move on
                        prngsess.save()

            self.stdout.write("%d peering interfaces found" % count['prngrtrifaces'])
            self.stdout.write("updated %d ipv4 peering sessions: %d new, %d provisioned" %
                              (count['prngsess4'], count['newsess4'], count['bgpprng4']))
            self.stdout.write("updated %d ipv6 peering sessions: %d new, %d provisioned" %
                              (count['prngsess6'], count['newsess6'], count['bgpprng6']))
            totals.update(count)

        # all done: print some stats
        self.stdout.write("finished updates for %d routers" % totals['rtrs'])
        self.stdout.write("%d peering interfaces found" % totals['prngrtrifaces'])
        self.stdout.write("updated %d ipv4 peering sessions: %d new, %d provisioned" %
                          (totals['prngsess4'], totals['newsess4'], totals['bgpprng4']))
        self.stdout.write("updated %d ipv6 peering sessions: %d new, %d provisioned" %
                          (totals['prngsess6'], totals['newsess6'], totals['bgpprng6']))

    def _update_state(self, prngsess, bgpprng):
        changed = False
        if bgpprng:
            # found a configured peering: update state fields
            if prngsess.provisioning_state != models.PeeringSession.PROV_COMPLETE:
                prngsess.provisioning_state = models.PeeringSession.PROV_COMPLETE
                changed = True
            # set admin_state
            if bgpprng['is_enabled']:
                if prngsess.admin_state != models.PeeringSession.ADMIN_START:
                    prngsess.admin_state = models.PeeringSession.ADMIN_START
                    changed = True
            else:
                if prngsess.admin_state != models.PeeringSession.ADMIN_STOP:
                    prngsess.admin_state = models.PeeringSession.ADMIN_STOP
                    changed = True
            # set operational_state
            if bgpprng['is_up']:
                if prngsess.operational_state != models.PeeringSession.OPER_ESTABLISHED:
                    prngsess.operational_state = models.PeeringSession.OPER_ESTABLISHED
                    changed = True
            else:
                if prngsess.operational_state == models.PeeringSession.OPER_ESTABLISHED:
                    prngsess.operational_state = models.PeeringSession.OPER_NONE
                    changed = True
            prngsess.accepted_prefixes = sum(
                bgpprng['address_family'][af]['accepted_prefixes'] for af in bgpprng['address_family']
            )
        else:
            # check if the peering session was previously provisioned, and reset if necessary
            if prngsess.provisioning_state != models.PeeringSession.PROV_NONE:
                prngsess.provisioning_state = models.PeeringSession.PROV_NONE
                changed = True
            prngsess.admin_state = models.PeeringSession.ADMIN_NONE
            prngsess.operational_state = models.PeeringSession.OPER_NONE
            prngsess.accepted_prefixes = 0
        if changed:
            try:
                prngsess.previous_state = prngsess.session_state
            except AttributeError:
                pass
            prngsess.state_changed = timezone.now()
        return changed
