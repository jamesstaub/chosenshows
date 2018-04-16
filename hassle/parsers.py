import datetime
import dateparser
import calendar
import re


class ParseSms:
    """
    Parse sms messages for dates, event categories

    """
    def __init__(self, sms_body):
        self.set_todays_date()

        self.get_tokens(sms_body)

        self.remove_salutations()

        self.date_reference = self.get_date()

        self.categories = self.get_categories()

        self.search_query = self.get_search_terms()

    def set_todays_date(self, today=None):

        # allow today to be overridden in tests
        self.today = today or datetime.datetime.today()
        self.today_weekday = calendar.day_name[self.today.weekday()].lower()

    def get_tokens(self, sms_body):
        """
        normalize tokens and bigrams from sms body
        """
        # only alpha chars
        regex = re.compile('[^a-zA-Z]')
        normalized_body = regex.sub(' ', sms_body).lower()

        self.tokens = [t for t in normalized_body.split(" ") if t]
        self.bigrams = [b for l in [normalized_body] for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]


    def remove_salutations(self):
        """
        separate out any salutation words, so they don't get
        used to search for events
        modifies self.tokens and self.bigrams
        """
        salutation_tokens =  ['hey',  'hi', 'yo', 'sup']
        salutation_bgs = [('hey', 'there'), ('whats','up')]
        self.tokens = [t for t in self.tokens if t not in salutation_tokens]
        self.bigrams = [bg for bg in self.bigrams if bg not in salutation_bgs]

    def get_date(self):
        """
        find references to relative or absolute dates in the text
        also remove the date references from self.tokens
        """

        today = self.today
        today_weekday = self.today_weekday

        tokens = self.tokens

        # convert tokens to  [[parsed_date, token]...]
        # the date elements are used for search date range, the tokens are used to remove
        # from them from search tems
        date_tokens = [[dateparser.parse(t, settings={'PREFER_DATES_FROM': 'future'}), t] for t in tokens]

        # remove tokens with no mention of dates
        date_tokens = [d for d in date_tokens if d[0]]

        # check edge cases
        if not date_tokens:
            if 'tonight' in tokens:
                # TODO: add filter for time
                search_date = dateparser.parse('today', settings={'PREFER_DATES_FROM': 'future'})
                date_tokens = [[search_date, 'tonight']]

            if 'this weekend' in self.bigrams:
                # if you're asking about the weekend while it is the weekend
                if today_weekday in ['friday', 'saturday']:
                    start_date = today

                else:
                    # if it's not yet the weekend
                    start_date = dateparser.parse('friday', settings={'PREFER_DATES_FROM': 'future'})

                end_date = dateparser.parse('sunday', settings={'PREFER_DATES_FROM': 'future'})
                date_tokens = [[start_date, 'this weekend'], [end_date, '']]

            if 'this week' in self.bigrams:
                start_date = dateparser.parse('today', settings={'PREFER_DATES_FROM': 'future'})
                end_date = dateparser.parse('saturday', settings={'PREFER_DATES_FROM': 'future'})
                date_tokens = [[start_date, 'this week'], [end_date, '']]

            # TODO:
            # if 'this month' in self.bigrams:
            #     start_date = dateparser.parse('today', settings={'PREFER_DATES_FROM': 'future'})
            #     last_day_of_month =
            #     date_tokens = [[start_date, 'this month'], [last_day_of_month, '']]

        search_dates = [d[0] for d in date_tokens]
        date_strings = [d[1] for d in date_tokens]

        self.remove_date_refs_from_tokens(date_strings)

        # set end date time to end of the day
        if len(search_dates) > 1:
            search_dates[1] = search_dates[1] + datetime.timedelta(hours=23, minutes=55)

        return search_dates

    def remove_date_refs_from_tokens(self, date_strings):
        self.tokens = [t for t in self.tokens if t not in date_strings]

    def get_categories(self):
        categories = ['music', 'art', 'film']
        return [t for t in self.tokens if t in categories]


    def get_search_terms(self):
        """
        return words to use as event search query
        by this point self.tokens has been normalized and
        filtered to remove dates and salutations
        """
        clean_search_string = ' '.join(self.tokens)

        # do other cleaning / NLP here

        return clean_search_string


    # #TODO fix this and filter stop words, try entity extraction
    # date_terms = [d[1] for d in dates]
    # excludes = date_terms + categories
    # search_tokens = [t for t in tokens if t not in excludes]
    #
    # if len(search_tokens) > 2:
    #     search_string = ' '.join(search_tokens)
    #     query_dict.update({"search": search_string})


    # is_question = sms_body.endswith('?')
    #
    # if is_question:
    #     is_location_request = sms_body.startswith('where')
    #
    #     is_time_request = sms_body.startswith('when')
