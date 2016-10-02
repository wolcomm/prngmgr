from django.conf.urls import url, include
from prngmgr.views import index, sessions, routers, interfaces, ixps, networks


urlpatterns = [
    url(r'^$', index.index, name="prngmgr-index"),
    url(r'^sessions/(filter/(?P<filter_field>\w+)/(?P<filter_arg>\w+))?$', sessions.sessions, name="prngmgr-sessions"),
    url(r'^networks/(?P<key>\d+)?$', networks.NetworksView.as_view(), name="prngmgr-networks"),
    url(r'^routers/(?P<rtr_id>\d+)?$', routers.routers, name="prngmgr-routers"),
    url(r'^ixps/(?P<ixp_id>\d+)?$', ixps.ixps, name="prngmgr-ixps"),
    url(r'^interfaces/(?P<if_id>\d+)?(?P<if_delete>/delete)?$', interfaces.interfaces, name="prngmgr-interfaces"),
    url(r'^api/', include('prngmgr.api.urls'))
]
