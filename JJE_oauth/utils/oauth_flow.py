from django.contrib.sites.models import Site
from JJE_App.settings import client_id, client_secret
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect

from JJE_oauth.models import UserToken

auth_url = "https://api.login.yahoo.com/oauth2/request_auth"
token_url = "https://api.login.yahoo.com/oauth2/get_token"


def create_oauth_session(_client_id=None, state=None, token=None):
    c_i = client_id
    if _client_id is not None:
        c_i = _client_id

    redirect_uri = "{}/oauth/callback".format(Site.objects.first().domain)

    access_token = token
    if token is not None:
        access_token = {'access_token': token}

    oauth = OAuth2Session(c_i, redirect_uri=redirect_uri, state=state,
                          token=access_token)
    return oauth


def start_oauth(request):
    oauth = create_oauth_session()
    authorization_url, state = oauth.authorization_url(auth_url)

    request.session['oauth_state'] = ""
    request.session['oauth_state'] = state

    return redirect(authorization_url)


def callback_oauth(request):
    x = "{}{}".format(Site.objects.first().domain, request.get_full_path())
    oauth = create_oauth_session(state=request.session['oauth_state'])
    token = oauth.fetch_token(token_url, client_secret=client_secret,
                              authorization_response=x)

    save_token(token, request)


def save_token(token, request, user_token=None):
    access_token = token.get("access_token")
    refresh_token = token.get("refresh_token")
    guid = token.get("xoauth_yahoo_guid")

    if user_token is None:
        user_token = UserToken()
        user_token.user = request.user

    user_token.client_id = client_id
    user_token.client_secret = client_secret
    user_token.access_token = access_token
    user_token.refresh_token = refresh_token
    user_token.user_guid = guid

    user_token.save()

    return


def refresh_token(request):
    user = request.user
    user_token = user.usertokens_set.first()

    _refresh_token(request, user_token)


def _refresh_token(request, user_token):
    extra = {
        'client_id': user_token.client_id,
        'client_secret': user_token.client_secret,
    }

    oauth = create_oauth_session(_client_id=user_token.client_id)
    new_token = oauth.refresh_token(
        token_url,
        refresh_token=user_token.refresh_token,
        **extra
    )

    save_token(new_token, request, user_token)
    return
