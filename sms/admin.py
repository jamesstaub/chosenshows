# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sms.models import Sms


class SMSAdmin(admin.ModelAdmin):
    list_display = ('sms_to', '__unicode__', )


try:
    admin.site.register(Sms, SMSAdmin)
except admin.sites.AlreadyRegistered:
    pass
