from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import datetime

# Create your models here.


class UserTokens(models.Model):
    """This is just for the API to collect and update the app"""
    date_created = models.DateTimeField(auto_now=True)
    client_id = models.TextField()
    client_secret = models.TextField()
    access_token = models.TextField()
    refresh_token = models.TextField()
    session_handle = models.TextField()
    user_guid = models.TextField()

    user = models.ForeignKey(User, default=None, blank=True, null=True)

    standings_token = models.BooleanField(default=False)

    def __repr__(self):
        return "<ID: {}>".format(self.id)

    @property
    def expired(self):
        if (self.date_created + datetime.timedelta(hours=1)) > timezone.now():
            return True
        else:
            return False