from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.

from JJE_Standings.utils import yahoo_api
from JJE_Standings.utils.yahoo_data import update_standings, build_team_data
from JJE_Standings.utils import get_standings_json, email_standings


class IndexView(View):
    def get(self, request):

        # yahoo_api.refresh_yahoo_token()

        return HttpResponse("")


class UpdateStandings(View):
    def get(self, request):
        # update_standings()
        email_standings()
        return HttpResponse(
            "<pre>{}</pre>".format(get_standings_json()))


class CreateTeams(View):
    def get(self, request):
        build_team_data()
        return HttpResponse("Done")
