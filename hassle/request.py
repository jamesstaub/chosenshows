import requests
import json

def get_events():
    """
    Request bostonhassle api
    save event data
    """

    root = 'https://bostonhassle.com/wp-json'
    endpoint = '/tribe/events/v1/events/'
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


        # else:
            # handle error
            # self.response.status_code = result.status_code
    except:
        print('Caught exception fetching url')

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
    endpoint = '/tribe/events/v1/tags'
    search = 'search={}'.format(query)
    params = 'orderby=count&order=desc'
    url = '{}{}?{}'.format(root, endpoint, params)
    r = requests.get(url)

    return r.json()
