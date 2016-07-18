from django.conf.urls import url
from prngmgr import views

urlpatterns = [
    url(r'^$', views.index, name="prngmgr-index"),
    url(r'^sessions/(filter/(?P<filter_field>\w+)/(?P<filter_arg>\w+))?$', views.sessions, name="prngmgr-sessions"),
    url(r'^networks/(?P<net_id>\d+)?$', views.networks, name="prngmgr-networks"),
    url(r'^routers/(?P<rtr_id>\d+)?$', views.routers, name="prngmgr-routers"),
    url(r'^ixps/(?P<ixp_id>\d+)?$', views.ixps, name="prngmgr-ixps"),
    url(r'^interfaces/(?P<if_id>\d+)?$', views.interfaces, name="prngmgr-interfaces"),
]
