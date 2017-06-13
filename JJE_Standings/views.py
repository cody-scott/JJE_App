from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.

from JJE_Standings.utils import yahoo_api
from JJE_Standings.utils.yahoo_data import get_standings

class IndexView(View):
    def get(self, request):

        # yahoo_api.refresh_yahoo_token()

        return HttpResponse("Index")

class UpdateStandings(View):
    def get(self, request):
        get_standings()
        return HttpResponse("Index")