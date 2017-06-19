from django.views.generic import View
from django.http import HttpResponse

from JJE_Standings.utils.yahoo_data import  build_team_data, update_standings
from JJE_Standings.utils import get_standings_json, email_standings, check_if_update_required


class IndexView(View):
    def get(self, request):
        return HttpResponse("")


class UpdateStandings(View):
    def get(self, request):
        # if check_if_update_required():
        update_standings(request)
        email_standings()

        return HttpResponse(
            "<pre>{}</pre>".format(get_standings_json()))


class CreateTeams(View):
    def get(self, request):
        build_team_data(request)
        return HttpResponse("Done")
