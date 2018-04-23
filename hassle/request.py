import requests
import json
import urllib
import logging
import datetime
import dateparser

from hassle.parsers import ParseSms

class EventResponse():
    def __init__(self, sms_body, send_response_to):
        search_params = self.get_search_params(sms_body)
        self.events = self.search_events(**search_params)
        self.response = self.get_response()

    # TODO:
    # NLP compares event api results to users prompt
    #     customize message if its not exactly what they aksed for
    #     (ie if no shows on the date they want, show future shows)
    #     check previous events sent to this user, dont send duplicates


    def get_search_params(self, sms_body):

        if sms_body:

            parsed_sms = ParseSms(sms_body)

            if parsed_sms.date:
                date_range = parsed_sms.date
                start_date = date_range[0]
            else:
                start_date = datetime.datetime.now()

            search_parameters = {"start_date": start_date.strftime("%Y-%m-%d")}

            categories = parsed_sms.categories or "hassle-shows"
            search_parameters.update({"categories": categories})

        else:
            search_parameters = {"categories": "hassle-shows"}

        return search_parameters


    def get_response(self):

        if self.events:
            self.events.sort(key=lambda tup: tup['start'])

            self.events = [self.format_events(event) for event in self.events]

            return  " | ".join(self.events)

        else:
            return 'couldnt find nothin'



    def filter_event_results(self, send_response_to):
        """
        Remove events from api response if they are from before today
        or if the recipient has already been notified of them
        """

        cutoff = datetime.datetime.today() - datetime.timedelta(hours=8)
        user = UserSmsProfile.objects.get(sms_number=send_response_to)

        # TODO: add a model for events, create association with SMS model
        # then check here if user has already received SMS containing these events
        self.events = [e for e in self.events if dateparser.parse(e['start']) > cutoff]


    def format_events(self, event):
        """
        validates that an event is not in the past,
        then formats text for sms response
        """
        date = dateparser.parse(event['start']).strftime('%m/%d')
        title = event['title']
        venue = event['venue']
        id = event['id']

        return u"""
            {} @ {} on {}
        """.format(date, title, venue)


    def search_events(self, **kwargs):

        root = 'https://bostonhassle.com/wp-json'
        endpoint = '/tribe/events/v1/events'

        # update params with other kwargs like start_date
        if kwargs is not None:
            params = urllib.parse.urlencode(kwargs)

        url = '{}{}?{}'.format(root, endpoint, params)

        try:
            response = requests.get(url)
            if response.status_code == 200:

                events = json.loads(response.text)['events']

                return [{
                    "id": e['id'],
                    "title": e['title'],
                    "venue":e['venue']['venue'],
                    "start": e['start_date'],
                    "tags": [t['slug'] for t in e['tags']]
                } for e in events if 'venue' in e['venue']]


            else:
                return []

        except Exception as e:
            logging.exception(e)

        return []


    # def search_tags(query):
    #     """
    #     returns a list of tag slugs matching search query
    #     """
    #     root = 'https://bostonhassle.com/wp-json'
    #     endpoint = '/tribe/events/v1/tags?search={}'.format(query)
    #     url = '{}{}'.format(root, endpoint)
    #     response = requests.get(url)
    #     tags = json.loads(response.content.decode('utf-8'))
    #
    #     # return tags
    #     return [t['slug'] for t in tags['tags']]
