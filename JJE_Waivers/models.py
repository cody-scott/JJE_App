from django.db import models
from django.utils import timezone
import datetime


class YahooTeam(models.Model):
    team_name = models.CharField(max_length=50)
    logo_url = models.TextField(blank=True)
    manager_name = models.CharField(max_length=200, blank=True)
    manager_email = models.EmailField(blank=True)

    def __str__(self):
        return self.team_name


class WaiverClaim(models.Model):

    team = models.ForeignKey(YahooTeam)

    claim_start = models.DateTimeField(default=timezone.now)

    add_player = models.CharField(max_length=255)
    add_position = models.CharField(max_length=255)

    add_LW = models.BooleanField(default=False)
    add_C = models.BooleanField(default=False)
    add_RW = models.BooleanField(default=False)
    add_D = models.BooleanField(default=False)
    add_G = models.BooleanField(default=False)
    add_Util = models.BooleanField(default=False)
    add_IR = models.BooleanField(default=False)

    drop_player = models.CharField(max_length=255)

    drop_LW = models.BooleanField(default=False)
    drop_C = models.BooleanField(default=False)
    drop_RW = models.BooleanField(default=False)
    drop_D = models.BooleanField(default=False)
    drop_G = models.BooleanField(default=False)
    drop_Util = models.BooleanField(default=False)
    drop_IR = models.BooleanField(default=False)

    over_claim_id = models.IntegerField(default=0)

    overclaimed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    # this should be a relationship to the team table
    # team_id = db.Column(db.Integer, db.ForeignKey('yahoo_teams.team_id'))

    def active_claim(self):
        now = timezone.now()
        return self.claim_start + datetime.timedelta(days=1) >= now

    def __str__(self):
        return self.add_player
