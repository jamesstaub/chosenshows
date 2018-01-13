# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone as tz


class Sms(models.Model):
    """
    Record all messages that are sent and received
    """
    sms_raw = models.CharField(max_length=1000)
    sms_body = models.CharField(max_length=2000)
    sms_to = models.CharField(blank=True, null=True, max_length=20)
    sms_from = models.CharField(blank=True, null=True, max_length=20)
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''

        self.created = tz.now()
        return super(Sms, self).save(*args, **kwargs)


    def __unicode__(self):
        return u"{time} | SMS:{sms_body} | To:{sms_to} | From:{sms_from}".format(
            sms_body=self.sms_body,
            sms_to = self.sms_to,
            sms_from = self.sms_from,
            time = tz.localtime(self.created).strftime('%b %d, %Y, %I:%M:%S %p'))

    class Meta:
        verbose_name_plural = "SMS received/sent"
