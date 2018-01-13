# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from MySQLpython.models import JSONField, Model
from django.db import models
from django.utils import timezone as tz 


class Event(models.Model):
    """
    Event listing scraped from boston hassle api
    """
    title = models.CharField(max_length=500)
    venue = models.CharField(max_length=500)
    start_date = models.DateTimeField('event start')
    created = models.DateTimeField()
    # tribe_id = models.IntegerField(primary_key=True)
    # tags = JSONField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''

        self.created = tz.now()
        return super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"""
            {} @ {} on {}
        """.format(self.title[:100], self.venue, self.start_date)
