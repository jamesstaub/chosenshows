import html
import requests
import json
import urllib
import logging
import datetime
import dateparser

from itertools import chain
from hassle.parsers import ParseSms
from sms.models import UserSmsProfile

class EventResponse():
    """
    initialize with an input query from sms body,
    calls ParseSMS to extract possible dates, cateogries, tags, search terms
    searches and formats events
    """

    def __init__(self, sms_body, send_response_to, limit=None):

        if sms_body:
            parsed_sms = ParseSms(sms_body)

            event_search_params = self.get_search_params(parsed_sms)

            self.events = self.search_events(**event_search_params)
            tags = self.search_tags(parsed_sms.search_query)

            if self.events:
                self.events = self.filter_event_results(self.events, tags)
                self.formatted_events = self.get_formatted_events(limit=limit)
                self.images = self.get_event_images(self.events, limit=limit)
                self.response = " | ".join(self.formatted_events)
            else:
                self.formatted_events = []
                self.images = []
                self.response = "cant find anything right now"

    # TODO:
    # NLP compares event api results to users prompt
    #     customize message if its not exactly what they aksed for
    #     (ie if no shows on the date they want, show future shows)
    #     check previous events sent to this user, dont send duplicates


    def get_search_params(self, parsed_sms):
        """
        takes instance of ParseSMS object,
        uses date + category references if they exist
        returns dictionary of search parameters for tribe events api
        """

        search_parameters = {}

        if parsed_sms.date:
            date_range = parsed_sms.date
            start_date = date_range[0]
            search_parameters.update({"start_date": start_date.strftime("%Y-%m-%d")})
        else:
            start_date = datetime.datetime.now()

        if parsed_sms.categories:
            search_parameters.update({"categories": parsed_sms.categories})

        return search_parameters


    def get_formatted_events(self, limit=None):
        """
        Returns a tuple of a string containing concatenated event info,
        and a list of event ids
        """

        self.events.sort(key=lambda tup: tup['start'])

        formatted_events = [self.format_events(event) for event in self.events]

        return formatted_events[:limit]



    def filter_event_results(self, events, tags, send_response_to=None):
        """
        Remove events from api response if
            they are from before today
            the recipient has already been notified of them

        Prioritize results if
            they match a tag
        """

        cutoff = datetime.datetime.today() - datetime.timedelta(hours=8)
        # user = UserSmsProfile.objects.get(sms_number=send_response_to)

        events = [e for e in events if dateparser.parse(e['start']) > cutoff]

        if tags:
            # comapre tag words on each event with tags that were found by the same search query
            tag_match_events = []
            events_tags = [[idx, [t.split('-') for t in e['tags']]] for idx, e in enumerate(events)]

            for event_tag in events_tags:
                event_index = event_tag[0]
                # flatten 2d list of tag words
                event_tags = list(chain.from_iterable( event_tag[1]))
                # find intersection of this event's tags and the tag results
                matched_tags = list(set(event_tags).intersection(tags))

                if matched_tags:
                    tag_match_events.append(event_index)


            if tag_match_events:
                # if we found events whose tags also match the tag filter_event_results
                # only return those events
                filtered_events = [events[i] for i in tag_match_events]

                print("""TAGS ON FOUND EVENTS: {}

                """.format(events_tags))
                print("""TAG SEARCH RESULTS: {}

                """.format(tags))
                print("""FILTERED EVENTS: {}

                """.format(filtered_events))

                events = filtered_events



        # TODO: add a model for events, create association with SMS model
        # then check here if user has already received SMS containing these events
        return events


    def format_events(self, event):
        """
        validates that an event is not in the past,
        then formats text for sms response
        """
        date = dateparser.parse(event['start']).strftime('%m/%d')
        title = event['title']
        venue = event['venue']
        id = event['id']

        formatted = u"""
            {} @ {} on {}
        """.format(date, title, venue)

        return html.unescape(formatted)


    def search_events(self, **kwargs):
        """
        takes search parameter kwargs and
        requests boston hassle events api
        returns list of serialized event detail strings
        """

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
                    "img": e['image']['sizes']['medium'],
                    "tags": [t['slug'] for t in e['tags']]
                } for e in events if e['image'] and 'venue' in e['venue']]

            else:
                return []

        except Exception as e:
            logging.exception(e)

        return []

    def get_event_images(self, events, limit):
        """
        returns a sorted list of images corresponding to self.events
        """
        return [e["img"] for e in events][:limit]


    def search_tags(self, query):
        """
        searches for tags that match a query
        returns a list of words split out from tag slug results
        """
        root = 'https://bostonhassle.com/wp-json'
        endpoint = '/tribe/events/v1/tags?search={}'.format(query)
        url = '{}{}'.format(root, endpoint)
        response = requests.get(url)
        tags = json.loads(response.content.decode('utf-8'))

        # return first matchin tag
        if tags and 'tags' in tags:
            # 2d list of slugs split by '-'
            slug_tokens = [t['slug'].split('-') for t in tags['tags']]
            return list(chain.from_iterable(slug_tokens))

        else:
            return []
