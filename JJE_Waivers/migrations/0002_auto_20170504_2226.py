# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 22:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('JJE_Waivers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waiverclaim',
            name='add_position',
        ),
        migrations.AddField(
            model_name='yahooteam',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]