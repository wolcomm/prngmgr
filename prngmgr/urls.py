from django.conf.urls import url, include
from prngmgr import classy_views
from prngmgr.views import routers, interfaces


urlpatterns = [
    url(r'^$', classy_views.IndexView.as_view(), name="prngmgr-index"),
    url(r'^sessions/(?P<pk>\d+)?$', classy_views.PeeringSessionsView.as_view(), name="prngmgr-sessions"),
    url(r'^networks/(?P<pk>\d+)?$', classy_views.NetworksView.as_view(), name="prngmgr-networks"),
    url(r'^ixps/(?P<pk>\d+)?$', classy_views.InternetExchangeView.as_view(), name="prngmgr-ixps"),
    url(r'^routers/(?P<rtr_id>\d+)?$', routers.routers, name="prngmgr-routers"),
    url(r'^interfaces/(?P<if_id>\d+)?(?P<if_delete>/delete)?$', interfaces.interfaces, name="prngmgr-interfaces"),
    url(r'^api/', include('prngmgr.api.urls'))
]
