from django.contrib import admin
from .models import WaiverClaim, YahooTeam


class WaiverClaimAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['claim_start']}),
        ('Team', {'fields': ["team"]}),
        ("Add Player Info", {'fields': [
            'add_player',
            'add_LW', 'add_C', 'add_RW', 'add_D', 'add_G', 'add_Util', 'add_IR',
        ]}),
        ("Drop Player Info", {'fields': [
            'drop_player',
            'drop_LW', 'drop_C', 'drop_RW', 'drop_D', 'drop_G', 'drop_Util', 'drop_IR',
        ]}),
    ]

    list_display = ['add_player', 'drop_player']


admin.site.register(WaiverClaim, WaiverClaimAdmin)
admin.site.register(YahooTeam)
