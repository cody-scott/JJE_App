from rest_framework import viewsets, permissions

from JJE_Main.api import serializer
from JJE_Main.models import YahooGUID, YahooTeam
from JJE_Main.utils import api_calls


# Returns GUID -> teams
class YahooTeamGUIDViewSetCurrentWeek(viewsets.ReadOnlyModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooCurrentGUIDSerializer

    filterset_fields = (
        'yahoo_guid',
    )

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # if self.request.user.is_authenticated():
        api_calls.update_teams(self.request)
        return YahooGUID.objects.all()


class YahooTeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YahooTeam.objects.all()
    serializer_class = serializer.YahooTeamSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            api_calls.update_teams(self.request)
        return YahooTeam.objects.all()
