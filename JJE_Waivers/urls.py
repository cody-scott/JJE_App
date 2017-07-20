from django.conf.urls import url, include
from . import views

from rest_framework.routers import DefaultRouter
from JJE_Waivers.api import views as api_views

router = DefaultRouter()
router.register(r'waiver_claims', api_views.WaiverClaimViewSet, 'waiver_claims')
router.register(r'active_claims', api_views.ActiveWaiverclaimViewSet, 'active_claims')

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^waiver_claim/new/$',
        views.WaiverClaimCreate.as_view(),
        name="waiver_claim-add"),
    url(r'^waiver_claim/overclaim=(?P<pk>[0-9]+)$',
        views.OverclaimCreate.as_view(),
        name="waiver_claim-overclaim"),
    url(r'^waiver_claim/cancel=(?P<pk>[0-9]+)$',
        views.CancelClaimView.as_view(),
        name="waiver_claim-cancel"),

    url(r'^api/', include(router.urls)),
]

# from rest_framework.schemas import get_schema_view
# schema_view = get_schema_view(title='Pastbin API')
# urlpatterns += [
#     url(r'^schema/$', schema_view)
# ]
