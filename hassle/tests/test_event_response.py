from django.test import TestCase
from hassle.request import EventResponse

class TestEventResponse(TestCase):

    def setUp(self):
        self.test_queries = ['music tonight']
        self.mockEvents = []
        self.mockTags = []


    def test_tag_response(self):
        """
        """

        for query in self.test_queries:
            response_data = EventResponse(query, None, 1)
            response_data.filter_event_results()
