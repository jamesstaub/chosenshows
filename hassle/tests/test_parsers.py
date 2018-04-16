# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import dateparser

from django.test import TestCase
from hassle.parsers import ParseSms

class TestParseres(TestCase):

    def setUp(self):
        # set the current day  to friday 4/20/2018
        self.today =  dateparser.parse('4/20/2018', settings={'PREFER_DATES_FROM': 'future'})

        self.test_messages = [
            "What's up tonight?",
            "shows tomorrow",
            "music this week",
            "experimental electronic music",
            # "garage rock this month",
            "yo whats up ",
            "films on thursday",
        ]

    def test_includes_date(self):
        """
        Tests that parser identifies messages with referene to
        a particular date
        """
