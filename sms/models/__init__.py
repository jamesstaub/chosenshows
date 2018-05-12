# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone as tz
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Sms(models.Model):
    """
    Record all messages that are sent and received
    from twilio endpoint
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

        if self.sms_to == '+13474427753':
            direction = 'from {}'.format(self.sms_from)
        elif self.sms_from == '+13474427753':
            direction = 'to {}'.format(self.sms_to)
        else:
            direction = ''

        return u"""
            "{sms_body}"
            {direction}  ______  {time}
            """.format(
            sms_body=self.sms_body,
            direction=direction,
            time = tz.localtime(self.created).strftime('%m-%d-%Y, %I:%M %p'))

    class Meta:
        verbose_name_plural = "SMS received/sent"


class UserSmsProfile(models.Model):
    """
    SMS settings and
    messages sent by and received by users
    """
    user = models.OneToOneField(User, related_name='user', null=True, on_delete=models.CASCADE)
    sms_number = models.CharField(max_length=12, blank=True, default='')
    event_tags = models.CharField(max_length=1000, blank=True, default='music')
    get_notifications = models.BooleanField(default=False, max_length=1000, blank=True)

    sms_sent = models.ForeignKey(Sms, related_name='sent_by_user', verbose_name='SMS messages sent by user', blank=True, null=True, on_delete=models.CASCADE)
    sms_received = models.ForeignKey(Sms, related_name='received_by_user', verbose_name='SMS messages received by user', blank=True, null=True, on_delete=models.CASCADE)


def create_sms_profile(sender, **kwargs):
    user = kwargs["instance"]

    if kwargs["created"]:
        sms_profile = UserSmsProfile(user=user)
        sms_profile.save()

post_save.connect(create_sms_profile, sender=User)
