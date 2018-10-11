from django.db import models
from django.utils import timezone
from JJE_Waivers.models import YahooTeam
import datetime

from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    user_email = instance.email
    username = user_email[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(
            username=username).exists():
        n += 1
        username = user_email[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username


class YahooStanding(models.Model):
    """Weekly standings from Yahoo"""
    date_created = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(YahooTeam, on_delete=models.SET_NULL, null=True)

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


    class Meta:
        ordering = ['current_standings', 'rank']
