from django.views.generic import View
from django.http import HttpResponse

from JJE_Standings.utils.yahoo_data import  build_team_data
from JJE_Standings.utils import get_standings_json, email_standings


class IndexView(View):
    def get(self, request):
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
