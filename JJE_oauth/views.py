from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.sites.models import Site

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from JJE_oauth.utils.oauth_flow import start_oauth, callback_oauth, refresh_token

from JJE_Waivers.utils import assign_user_teams_from_token


@method_decorator(login_required, name='dispatch')
class OAuthStart(View):
    def get(self, request):
        return start_oauth(request)


@method_decorator(login_required, name='dispatch')
class OAuthCallback(View):
    def get(self, request):
        callback_oauth(request)
        assign_user_teams_from_token(request)
        return redirect(Site.objects.first().domain)


@method_decorator(login_required, name='dispatch')
class OAuthRefresh(View):
    def get(self, request):
        refresh_token(request)
        return redirect(Site.objects.first().domain)
