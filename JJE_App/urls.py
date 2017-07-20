"""JJE_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from JJE_App.settings import DEBUG

from rest_framework.routers import DefaultRouter
from JJE_Waivers.api import views as api_views_1
from JJE_Standings.api import views as api_views_2

router = DefaultRouter()
router.register(r'waiver_claims', api_views_1.WaiverClaimViewSet, 'all_waiver_claims')
router.register(r'active_claims', api_views_1.ActiveWaiverclaimViewSet, 'active_claims')
router.register(r'all_standings', api_views_2.StandingsViewSet, 'all_standings')
router.register(r'standings', api_views_2.ActiveStandingsViewSet, 'standings')

admin.site.site_title = "JJE Admin"
admin.site.site_header = "JJE Admin"
urlpatterns = [
    url(r'', include('JJE_Waivers.urls'), name="main"),
    url(r'^standings/', include("JJE_Standings.urls"), name="standings"),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^oauth/', include('JJE_oauth.urls'), name="JJE_oauth"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
]


if DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
