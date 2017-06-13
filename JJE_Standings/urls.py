from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='standings_index'),
    url(r'^update$', views.UpdateStandings.as_view(), name="update_standings"),
]
