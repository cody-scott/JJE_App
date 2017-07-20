from rest_framework import serializers


from JJE_Standings.models import YahooStanding

class YahooStandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooStanding
        fields = (
            'team',
            'rank',
            'stat_point_total',
            'standings_week',
        )
