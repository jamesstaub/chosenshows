import requests
import json
import urllib
import logging

from hassle.parsers import parse_message_terms

def render_response(sms_body, send_response_to):

    search_terms = parse_message_terms(sms_body)
    events = get_events(search_terms)

    if events:
        event = events[-1]
    else:
        print(events)

    response_body = """
        {} @ {} on {}
    """.format(event['title'], event['venue'], event['start'])

    return response_body


def get_events(search_terms):
    """
    Request bostonhassle api
    """

    root = 'https://bostonhassle.com/wp-json'

    if bool(search_terms):
        start_date = search_terms['start_date'] if 'start_date' in search_terms
        categories = search_terms['categories'] if 'categories' in search_terms
    endpoint = '/tribe/events/v1/'
    url = '{}{}'.format(root, endpoint)

    try:
        result = requests.get(url)
        if result.status_code == 200:

            events = json.loads(result.text)['events']

            return [{
                "id": e['id'],
                "title": e['title'],
                "venue":e['venue']['venue'],
                "start": e['start_date'],
                "tags": [t['slug'] for t in e['tags']]
            } for e in events if 'venue' in e['venue']]


        else:
            handle error
            self.response.status_code = result.status_code
    except Exception as e:
        logging.exception(e)

    return []

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
    r = requests.get(url)

    return r.json()
