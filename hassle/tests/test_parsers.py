# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import dateparser
import datetime
import calendar
from django.test import TestCase
from hassle.parsers import ParseSms

class TestParseres(TestCase):

    def setUp(self):
        today = datetime.datetime.today().replace(hour=0, minute=0)
        parser_future = {'PREFER_DATES_FROM': 'future', 'TIMEZONE': 'US/Eastern'}
        upcoming_thursday = dateparser.parse(calendar.day_name[3],settings=parser_future)

        self.test_messages = [
            # ("any music tonight?",  datetime.datetime.today()),
            ("any music today?",  today),
            ("shows tomorrow", today + datetime.timedelta(days=1)),
            ("films on thursday", upcoming_thursday),
            ("whats going on", []) #no dates returned
            # ("yo whats up ", ),
            # ("experimental electronic music", ),
            # ("garage rock this month", ),
        ]

    def test_includes_date(self):
        """
        Tests that parser identifies messages with reference to
        a particular date
        """

        for msg, expected in self.test_messages:
            parsed = ParseSms(msg)

            comment = "testing {}".format(msg)
            if parsed.date:
                self.assertEqual(parsed.date[0].date(), expected.date(), comment)
            else:
                # when expecting None
                self.assertEqual(parsed.date, expected, comment)
