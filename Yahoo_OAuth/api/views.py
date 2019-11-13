from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes

from Yahoo_OAuth.utils import yahoo_requests


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_standings(request):
    res, s_code = yahoo_requests.get_standings(request)
    return Response(res, s_code)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_team(request):
    res, s_code = yahoo_requests.get_user_teams(request)
    return Response(res, s_code)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_teams(request):
    res, s_code = yahoo_requests.get_teams(request)
    return Response(res, s_code)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_player(request, *args, **kwargs):
    res, s_code = yahoo_requests.get_player(request, args, kwargs)
    return Response(res, s_code)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_players(request, *args, **kwargs):
    res, s_code = yahoo_requests.get_players(request, args, kwargs)
    return Response(res, s_code)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_roster(request, *args, **kwargs):
    res, s_code = yahoo_requests.get_team_roster(request, args, kwargs)
    return Response(res, s_code)
