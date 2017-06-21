from django.contrib import admin

# Register your models here.
from JJE_oauth.models import UserToken


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'standings_token']

    fieldsets = [
        ('Standings', {'fields': ['user', 'standings_token']})
    ]

admin.site.register(UserToken, UserTokenAdmin)
