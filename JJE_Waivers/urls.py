from django.conf.urls import url, include
from . import views


from JJE_Waivers.api import views as waivers_api
from rest_framework.routers import SimpleRouter
router = SimpleRouter()


router.register(r'active_claims', waivers_api.ActiveWaiverclaimViewSet, base_name='active_claims')
router.register(r'all_claims', waivers_api.WaiverClaimViewSet, base_name='all_claims')

router.register(r'new', waivers_api.CreateNewWaiverViewSet, base_name='new_api_claim')
router.register(r'overclaim', waivers_api.CreateOverclaimViewSet, base_name='overclaim_api_claim')
router.register(r'cancel', waivers_api.CancelClaimViewSet, base_name='cancel_api_claim')


urlpatterns = [
    url(r'api/', include(router.urls))
]

urlpatterns += [
    # url(r'^$', views.MyView.as_view(), name='index'),
    url(r'^$', views.IndexView.as_view(), name='waivers_index'),
    url(r'^new/',
        views.WaiverClaimCreate.as_view(),
        name="waiver_claim-add"),

    url(r'^overclaim=(?P<pk>[0-9]+)$',
        views.OverclaimCreate.as_view(),
        name="waiver_claim-overclaim"),
    url(r'^cancel=(?P<pk>[0-9]+)$',
        views.CancelClaimView.as_view(),
        name="waiver_claim-cancel"),
]
