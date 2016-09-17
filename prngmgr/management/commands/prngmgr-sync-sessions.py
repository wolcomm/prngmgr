from django.core.management.base import BaseCommand, CommandError
from collections import Counter
from prngmgr.settings import *
from prngmgr.models.models import *
from prngmgr.snmp import *

class Command(BaseCommand):
    help = 'Queries peering routers for BGP related SNMP data'

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
        me = Network.objects.get(asn=MY_ASN)

        # create list of PeeringRouters and a totals counter
        rtrs = []
        totals = Counter()

        if options['router']:
            # check if we were given a router to query
            try:
                rtr = PeeringRouter.objects.get(hostname=options['router'])
            except PeeringRouter.DoesNotExist:
                raise CommandError('PeeringRouter "%s" does not exist' % options['router'])
            rtrs.append(rtr)
        else:
            # fallback to querying all PeeringRouters
            for rtr in PeeringRouter.objects.all():
                rtrs.append(rtr)

        for rtr in rtrs:

            # create per router counter and update rtr count
            count = Counter()
            totals['rtrs'] += 1

            # collect cbgpPeer2Table via SNMP
            self.stdout.write( "Querying %s via SNMP" % rtr.hostname )
            bgptable = get_bgp_table(rtr.hostname)

            # get all PeeringRouterIXInterfaces on router
            ifaces = PeeringRouterIXInterface.objects.filter(prngrtr=rtr)
            for iface in ifaces:

                # update count
                count['prngrtrifaces'] += 1

                # get all NetworkIXLans on a common IX
                peer_netixlans = NetworkIXLan.objects.filter(ixlan=iface.netixlan.ixlan)
                for peer_netixlan in peer_netixlans:

                    # check that we're not peering with ourselves
                    if peer_netixlan.net == me:
                        continue

                    # check for valid ipv4 peering info
                    if iface.netixlan.ipaddr4 and peer_netixlan.ipaddr4:

                        # update count
                        count['prngsess4'] += 1

                        # found an ipv4 session
                        prngsessions = PeeringSession.objects.filter(af=PeeringSession.AF_IPV4).filter(peer_netixlan=peer_netixlan).filter(prngrtriface=iface)
                        if prngsessions.exists():

                            # PeeringSession exists: retrieving it
                            prngsess = prngsessions[0]

                        else:

                            # PeeringSession doesn't exist: creating it
                            prngsess = PeeringSession(af=PeeringSession.AF_IPV4, peer_netixlan=peer_netixlan, prngrtriface=iface)

                        # search for a bgptable entry
                        bgpprng = None
                        for entry in bgptable:
                            if ( bgptable[entry]['cbgpPeer2Type'] == prngsess.af and
                                 bgptable[entry]['cbgpPeer2RemoteAddr'] == prngsess.peer_netixlan.ipaddr4 and
                                 bgptable[entry]['cbgpPeer2RemoteAs'] == prngsess.peer_netixlan.asn ):
                                # found a configured peering
                                count['bgpprng4'] += 1
                                bgpprng = bgptable[entry]

                        # update PeeringSession from bgp peering state
                        self._update_state(prngsess, bgpprng)

                        # save and move on
                        prngsess.save()

                    # check for valid ipv6 peering info
                    if iface.netixlan.ipaddr6 and peer_netixlan.ipaddr6:

                        # update count
                        count['prngsess6'] += 1

                        # found an ipv6 session
                        prngsessions = PeeringSession.objects.filter(af=PeeringSession.AF_IPV6).filter(peer_netixlan=peer_netixlan).filter(prngrtriface=iface)
                        if prngsessions.exists():

                            # PeeringSession exists: retrieving it
                            prngsess = prngsessions[0]
                        else:

                            # PeeringSession doesn't exist: creating it
                            prngsess = PeeringSession(af=PeeringSession.AF_IPV6, peer_netixlan=peer_netixlan, prngrtriface=iface)

                        # search for a bgptable entry 
                        bgpprng = None
                        for entry in bgptable:
                            if ( bgptable[entry]['cbgpPeer2Type'] == prngsess.af and
                                 bgptable[entry]['cbgpPeer2RemoteAddr'] == prngsess.peer_netixlan.ipaddr6 and
                                 bgptable[entry]['cbgpPeer2RemoteAs'] == prngsess.peer_netixlan.asn ):
                                # found a configured peering
                                count['bgpprng6'] += 1
                                bgpprng = bgptable[entry]

                        # update PeeringSession from bgp peering state
                        self._update_state(prngsess, bgpprng)

                        # save and move on
                        prngsess.save()

            self.stdout.write( "%d peering interfaces found" % count['prngrtrifaces'] )
            self.stdout.write( "updated %d ipv4 peering sessions: %d provisioned in bgp" % (count['prngsess4'], count['bgpprng4']) )
            self.stdout.write( "updated %d ipv6 peering sessions: %d provisioned in bgp" % (count['prngsess6'], count['bgpprng6']) )
            totals.update(count)

        # all done: print some stats
        self.stdout.write( "finished updates for %d routers" % totals['rtrs'] )
        self.stdout.write( "%d peering interfaces found" % totals['prngrtrifaces'] )
        self.stdout.write( "updated %d ipv4 peering sessions: %d provisioned in bgp" % (totals['prngsess4'], totals['bgpprng4']) )
        self.stdout.write( "updated %d ipv6 peering sessions: %d provisioned in bgp" % (totals['prngsess6'], totals['bgpprng6']) )

    def _update_state(self, prngsess, bgpprng):
        if bgpprng:
            # found a configured peering: update state fields
            prngsess.provisioning_state = PeeringSession.PROV_COMPLETE
            prngsess.admin_state = bgpprng['cbgpPeer2AdminStatus']
            prngsess.operational_state = bgpprng['cbgpPeer2State']
        else:
            # check if the peering session was previously provisioned, and reset if necessary
            if prngsess.provisioning_state == PeeringSession.PROV_COMPLETE:
                prngsess.provisioning_state = PeeringSession.PROV_NONE
            prngsess.admin_state = PeeringSession.ADMIN_NONE
            prngsess.operational_state = PeeringSession.OPER_NONE
        return

