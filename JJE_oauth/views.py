from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.sites.models import Site

# Create your views here.
from JJE_oauth.utils.new_oauth_flow import start_oauth, callback_oauth, refresh_token


class OAuthStart(View):
    def get(self, request):
        return start_oauth(request)


class OAuthCallback(View):
    def get(self, request):
        callback_oauth(request)
        # site = request.get_current_site()
        return redirect(Site.objects.first().domain)


class OAuthRefresh(View):
    def get(self, request):
        refresh_token(request)
        return redirect(Site.objects.first().domain)
