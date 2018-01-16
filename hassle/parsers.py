import dateparser

def parse_message_terms(sms_body):

    # remove double and trailing whitespace
    sms_body = ' '.join(sms_body.split())

    # TODO: separate stopwords
    tokens = sms_body.split(' ')

    dates = [[dateparser.parse(t, settings={'PREFER_DATES_FROM': 'future'}), t] for t in tokens]

    #remove None values then get first mention
    search_date = next(iter([d[0] for d in dates if d[0]]), None)

    if not search_date:
        # TODO add 'this week' & support sending multiple results when appropriate
        # hacky way to later remove the date string from the rest of the texts
        if 'tonight' in sms_body:
            search_date = dateparser.parse('today', settings={'PREFER_DATES_FROM': 'future'})
            dates = [[search_date, 'today']]

        if 'weekend' in sms_body:
            search_date = dateparser.parse('friday', settings={'PREFER_DATES_FROM': 'future'})
            dates = [[search_date, 'weekend']]


    categories = ['music', 'art', 'film']
    search_category = [t for t in tokens if t in categories]

    query_dict = {
        "start_date": search_date,
        "categories": search_category,
    }

    # #TODO fix this and filter stop words, try entity extraction
    # date_terms = [d[1] for d in dates]
    # excludes = date_terms + categories
    # search_tokens = [t for t in tokens if t not in excludes]
    #
    # if len(search_tokens) > 2:
    #     search_string = ' '.join(search_tokens)
    #     query_dict.update({"search": search_string})

    query_dict = {k: v for k, v in query_dict.items() if v is not None}

    return query_dict

    # is_question = sms_body.endswith('?')
    #
    # if is_question:
    #     is_location_request = sms_body.startswith('where')
    #
    #     is_time_request = sms_body.startswith('when')
