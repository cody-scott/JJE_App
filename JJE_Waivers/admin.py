from django.contrib import admin
from .models import WaiverClaim, YahooTeam
from JJE_Standings.models import YahooStanding


class WaiverClaimAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = [
        ('Claim ID', {'fields': ['id']}),
        (None, {'fields': ['claim_start']}),
        ('Team', {'fields': ["team"]}),
        ('Overclaim/Cancelled', {'fields': ["overclaimed", "over_claim_id", "cancelled"]}),
        ("Add Player Info", {'fields': [
            'add_player',
            'add_LW', 'add_C', 'add_RW', 'add_D', 'add_G', 'add_Util', 'add_IR',
        ]}),
        ("Drop Player Info", {'fields': [
            'drop_player',
            'drop_LW', 'drop_C', 'drop_RW', 'drop_D', 'drop_G', 'drop_Util', 'drop_IR',
        ]}),
    ]
    list_display = ['pk', 'add_player', 'drop_player', 'team', 'active_claim']


class StandingsAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ("Stat Totals", {'fields': [
    #         'stat_1', 'stat_2', 'stat_3', 'stat_4', 'stat_5', 'stat_8', 'stat_12',
    #         'stat_31', 'stat_19', 'stat_22', 'stat_23', 'stat_25',
    #         'stat_24', 'stat_26', 'stat_27'
    #     ]}),
    #     ("Stat Points", {'fields': [
    #         'stat_points_1', 'stat_points_2', 'stat_points_3', 'stat_points_4', 'stat_points_5', 'stat_points_8', 'stat_points_12',
    #         'stat_points_31', 'stat_points_19', 'stat_points_22', 'stat_points_23', 'stat_points_25',
    #         'stat_points_24', 'stat_points_26', 'stat_points_27'
    #     ]})
    # ]
    list_display = ['team', 'rank', 'stat_point_total', 'current_standings', 'standings_week']
    ordering = ['-standings_week', 'rank']
    list_per_page = 12


admin.site.register(WaiverClaim, WaiverClaimAdmin)
admin.site.register(YahooTeam)
admin.site.register(YahooStanding, StandingsAdmin)
