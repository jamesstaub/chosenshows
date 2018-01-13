# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sms.models import Sms

try:
    admin.site.register(Sms)
except admin.sites.AlreadyRegistered:
    pass
