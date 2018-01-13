from hassle.request import get_events

def respond_to_user(sms_body, send_response_to):

    events = get_events()

    if events:
        event = events[-1]
    else:
        print(events)

    response_body = """
        {} @ {} on {}
    """.format(event['title'], event['venue'], event['start'])

    return response_body


def parse_message_terms(sms_body):

    
    date
