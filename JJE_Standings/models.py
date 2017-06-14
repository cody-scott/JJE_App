from django.db import models
from django.utils import timezone
from JJE_Waivers.models import YahooTeam
import datetime


class YahooStanding(models.Model):
    """Weekly standings from Yahoo"""
    date_created = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(YahooTeam)

    rank = models.IntegerField()
    stat_point_total = models.FloatField()

    stat_1 = models.FloatField()
    stat_2 = models.FloatField()
    stat_3 = models.FloatField()
    stat_4 = models.FloatField()
    stat_5 = models.FloatField()
    stat_8 = models.FloatField()
    stat_12 = models.FloatField()
    stat_31 = models.FloatField()
    stat_19 = models.FloatField()
    stat_22 = models.FloatField()
    stat_23 = models.FloatField()
    stat_25 = models.FloatField()
    stat_24 = models.FloatField()
    stat_26 = models.FloatField()
    stat_27 = models.FloatField()

    stat_points_1 = models.FloatField()
    stat_points_2 = models.FloatField()
    stat_points_3 = models.FloatField()
    stat_points_4 = models.FloatField()
    stat_points_5 = models.FloatField()
    stat_points_8 = models.FloatField()
    stat_points_12 = models.FloatField()
    stat_points_31 = models.FloatField()
    stat_points_19 = models.FloatField()
    stat_points_22 = models.FloatField()
    stat_points_23 = models.FloatField()
    stat_points_25 = models.FloatField()
    stat_points_24 = models.FloatField()
    stat_points_26 = models.FloatField()
    stat_points_27 = models.FloatField()

    standings_week = models.IntegerField()

    current_standings = models.BooleanField(default=False)

    def __str__(self):
        return "<id: {}>".format(self.team)


class YahooKey(models.Model):
    """This is just for the API to collect and update the app"""
    date_created = models.DateTimeField(auto_now=True)
    consumer_key = models.TextField()
    consumer_secret = models.TextField()
    access_token = models.TextField()
    access_secret_token = models.TextField()
    session_handle = models.TextField()
    user_guid = models.TextField()

    def __repr__(self):
        return "<ID: {}>".format(self.id)

    @property
    def expired(self):
        if (self.date_created + datetime.timedelta(hours=1)) > timezone.now():
            return True
        else:
            return False