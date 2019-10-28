from Yahoo_OAuth.utils.oauth_flow import refresh_user_token, create_oauth_session

from django.conf import settings
from urllib.parse import urlencode


from JJE_App.settings import BASE_DIR
import os


def _get_local(file_name):
    # todo remove this
    pt = os.path.join(BASE_DIR, f'Development\\test_files\\{file_name}')
    with open(pt, 'r') as fl:
        return fl.read(), 200


def create_session(token):
    token = refresh_user_token(token)
    oauth = create_oauth_session(_client_id=token.client_id,
                                 token=token.access_token)
    return oauth


def get_standings(request):
    # return _get_local('standings.txt')

    token = request.user.usertoken_set.first()
    # token = UserToken.objects.get(standings_token=True)
    yahoo_obj = create_session(token)
    r = request_standings(yahoo_obj)
    return r['results'], r["status_code"]


def get_teams(request):
    # return _get_local('standings.txt')

    token = request.user.usertoken_set.first()
    yahoo_obj = create_session(token)
    r = request_teams(yahoo_obj)
    return r['results'], r["status_code"]


def get_user_teams(request):
    # return _get_local('userteams.txt')

    token = request.user.usertoken_set.first()
    yahoo_obj = create_session(token)
    r = request_teams(yahoo_obj, True)
    return r['results'], r["status_code"]


def get_player(request, *args, **kwargs):
    q_params = request.query_params
    player_id = q_params.get("player_id")
    if player_id is None:
        return ["Error with player id"], 400
    sub_r = {c: q_params[c] for c in q_params if c != "player_id"}

    token = request.user.usertoken_set.first()
    yahoo_obj = create_session(token)

    res = request_player(yahoo_obj, player_id, sub_r)

    return res['results'], res["status_code"]


def get_players(request, *args, **kwargs):
    q_params = request.query_params
    token = request.user.usertoken_set.first()
    yahoo_obj = create_session(token)

    res = request_players(yahoo_obj, q_params)

    return res['results'], res["status_code"]


def _get_request(yahoo_obj, url):
    result = yahoo_obj.request("get", url)
    results, status_code = result.text, result.status_code

    return {"results": result.text, "status_code": status_code}


def request_standings(yahoo_obj):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/standings"
    return _get_request(yahoo_obj, url)


def request_roster(yahoo_obj, team_id):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/{settings.LEAGUE_ID}.t.{team_id}/roster/players"
    return _get_request(yahoo_obj, url)


def request_players(yahoo_obj, player_dict):
    player_args = urlencode(player_dict)
    player_args = player_args.replace("&", ";")
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/players;{player_args}/stats"
    return _get_request(yahoo_obj, url)


def request_player(yahoo_obj, player_id, sub_resources=None):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/players;player_keys=nhl.p.{player_id}/stats"
    if sub_resources is not None:
        sr = urlencode(sub_resources)
        sr = sr.replace("&", ";")
        url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/players;player_keys=nhl.p.{player_id};{sr}/stats"
        # url += f';{",".join(sr)}'
    return _get_request(yahoo_obj, url)


def request_teams(yahoo_obj, use_login=False):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/teams"
    if use_login:
        url += ';use_login=1'

    return _get_request(yahoo_obj, url)
