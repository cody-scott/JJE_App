from rest_framework import serializers

from JJE_Main.models import YahooTeam
from JJE_Waivers.models import WaiverClaim


class YahooTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooTeam
        fields = (
            'id',
            'team_id',
            'team_name',
            'logo_url',
        )


class WaiverClaimSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamSerializer()

    class Meta:
        model = WaiverClaim
        fields = (
            'id', 'yahoo_team', 'claim_start',
            'add_player', 'add_LW', 'add_C', 'add_RW', 'add_D', 'add_G', 'add_Util', 'add_IR',
            'drop_player', 'drop_LW', 'drop_C', 'drop_RW', 'drop_D', 'drop_G', 'drop_Util', 'drop_IR',
            'over_claim_id', 'overclaimed', 'cancelled', 'claim_message',
            'get_position_add', 'get_position_drop',
            'claim_end_iso', 'claim_end_normal',
            'active_claim',
        )
        read_only_fields = (
            'active_claim',
        )


class WaiverClaimCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiverClaim
        fields = (
            'yahoo_team',
            'add_player', 'add_LW', 'add_C', 'add_RW', 'add_D', 'add_G', 'add_Util', 'add_IR',
            'drop_player', 'drop_LW', 'drop_C', 'drop_RW', 'drop_D', 'drop_G', 'drop_Util', 'drop_IR',
            'claim_message',
        )


class WaiverOverclaimCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiverClaim
        fields = (
            'yahoo_team',
            'over_claim_id',
            'drop_player', 'drop_LW', 'drop_C', 'drop_RW', 'drop_D', 'drop_G', 'drop_Util', 'drop_IR',
            'claim_message',
        )


class WaiverCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiverClaim
        fields = (
            'id',
            'yahoo_team',
        )
