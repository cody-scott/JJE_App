from rest_framework import viewsets, mixins, permissions

from JJE_Waivers.api.serializer import WaiverClaimSerializer, \
    WaiverClaimCreateSerializer, WaiverOverclaimCreateSerializer, WaiverCancelSerializer
from JJE_Waivers.models import WaiverClaim

from JJE_Waivers.utils import jje_waiver_functions
from JJE_Waivers.api import jje_api_functions
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta


class WaiverClaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WaiverClaim.objects.all()
    serializer_class = WaiverClaimSerializer


class ActiveWaiverclaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WaiverClaim.objects.all()
    serializer_class = WaiverClaimSerializer

    def get_queryset(self):
        return jje_waiver_functions.get_active_claims()


class CreateNewWaiverViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = WaiverClaim.objects.all()
    serializer_class = WaiverClaimCreateSerializer

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        res, status = jje_api_functions.validate_new_claim(request, request.data)
        if type(res) == WaiverClaim:
            res = WaiverClaimSerializer(instance=res).data
        return Response(res, status)


class CreateOverclaimViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = WaiverClaim.objects.all()
    serializer_class = WaiverOverclaimCreateSerializer

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        res, status = jje_api_functions.validate_over_claim(request, request.data)
        if type(res) == WaiverClaim:
            res = WaiverClaimSerializer(instance=res).data
        return Response(res, status)


class CancelClaimViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = WaiverClaim.objects.all()
    serializer_class = WaiverCancelSerializer

    def update(self, request, *args, **kwargs):
        res, status = jje_api_functions.validate_cancel_claim(request, kwargs.get('pk'))
        if type(res) == WaiverClaim:
            res = WaiverClaimSerializer(instance=res).data
        return Response(res, status)
