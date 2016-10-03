from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from prngmgr.api import views


router = DefaultRouter()
router.register(r'org', views.OrganizationViewSet)
router.register(r'fac', views.FacilityViewSet)
router.register(r'net', views.NetworkProxyViewSet)
router.register(r'ix', views.InternetExchangeProxyViewSet)
router.register(r'ixfac', views.InternetExchangeFacilityViewSet)
router.register(r'ixlan', views.IXLanViewSet)
router.register(r'ixpfx', views.IXLanPrefixViewSet)
router.register(r'poc', views.NetworkContactViewSet)
router.register(r'netixlan', views.NetworkIXLanViewSet)
router.register(r'router', views.PeeringRouterViewSet)
router.register(r'interface', views.PeeringRouterIXInterfaceViewSet)
router.register(r'session', views.PeeringSessionViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
