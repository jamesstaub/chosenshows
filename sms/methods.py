""" dialog scenario

user texts "hello, hey, hi, sup, whats up, yo"

    app replies "hey I'm hassle showbot, you can ask me for deets about upcoming boston hassle events"
    "try genre tags or band names like {pull tags from upcoming shows} "

user texts "shows"
    if includes {tonight, tomorrow, this week etc}
        filter results by indicated date

    app replies "next upcoming show is... txt more for another listing ? "

        user texts "more"

        app replies "another show listing ... you can specify genre or artists"

"""
