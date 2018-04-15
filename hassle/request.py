import requests
import json
import urllib
import logging

from hassle.parsers import parse_message_terms

def render_response(sms_body, send_response_to):
    if sms_body:
        search_terms = parse_message_terms(sms_body)
        events = search_events(search_terms)

    else:
        events = search_events('music')


    if events:
        event = events[0]

        response_body = """
            {} @ {} on {}
        """.format(event['title'], event['venue'], event['start'])

    else:
        response_body = 'couldnt find nothin'

    return response_body


# def get_events(search_terms):
#     """
#     Request bostonhassle api
#     """
#
#     root = 'https://bostonhassle.com/wp-json'
#
#     if bool(search_terms):
#         if 'start_date' in search_terms:
#             start_date = search_terms['start_date']
#         if 'categories' in search_terms:
#             categories = search_terms['categories']
#
#     endpoint = '/tribe/events/v1/'
#
#     url = '{}{}'.format(root, endpoint)
#
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#
#             events = json.loads(response.text)['events']
#
#             return [{
#                 "id": e['id'],
#                 "title": e['title'],
#                 "venue":e['venue']['venue'],
#                 "start": e['start_date'],
#                 "tags": [t['slug'] for t in e['tags']]
#             } for e in events if 'venue' in e['venue']]
#
#
#         else:
#             # handle error
#             self.response.status_code = response.status_code
#
#     except Exception as e:
#         logging.exception(e)
#
#     return []

def search_tags(query):
    """
    returns a list of tag slugs matching search query
    """
    root = 'https://bostonhassle.com/wp-json'
    endpoint = '/tribe/events/v1/tags?search={}'.format(query)
    url = '{}{}'.format(root, endpoint)
    response = requests.get(url)
    tags = json.loads(response.content.decode('utf-8'))

    # return tags
    return [t['slug'] for t in tags['tags']]

def search_events(query):
    root = 'https://bostonhassle.com/wp-json'
    endpoint = '/tribe/events/v1/events'

    params = urllib.parse.urlencode({
        "categories": "chosen-shows",
        "search": query,
    })

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
            # handle error
            self.response.status_code = response.status_code

    except Exception as e:
        logging.exception(e)

    return []
